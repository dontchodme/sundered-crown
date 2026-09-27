#!/usr/bin/env python3
"""COROLLARY'S THREE VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v88.

    python corollary_voice_lab.py --game ../02-chain/sc-corollary.html

v80 §4 SOUND, every word of it: "cast -- a rune-chime, 0.3s; the echo -- the
sword's own strike voice, reversed (a rising "whoom"), quieter; the hex -- its
snap."  Rick, 2026-09-26, for stage 4's picture and sound: "you pick i
overrule". So this lab does not offer a spread for him to choose from -- it
renders three to five candidates a voice beside CONTROLS that can come back
wrong, prints the numbers each pick is made on, and PICKS by a rule written
in this file (`pick_*` below). He overrules from one clip.

THE CONTROLS, and what each one is for:

  rune-crack      what Axiom's cast plays TODAY (it has no arm, so it falls
                  through to the shared fallback eleven relics use). The cast
                  pick must be CLEARLY NOT this.
  hit @ dmg       the sword's own strike voice at the echo's damage -- the
                  thing the echo is the reverse of, and what "quieter" is
                  measured against, at the SAME dmg.
  literal         the hit rendered dry, its samples REVERSED, and played back
                  through the chain. A reference, not a candidate: it needs an
                  async render, and `cinema_clip.renderAudio` / `render.py`
                  rebuild the synth synchronously with `Object.create`, so a
                  shipped literal reversal would be SILENT in every clip. The
                  candidates are built SYNCHRONOUSLY from `_sweep` / `_tone` /
                  `_burst` and are measured AGAINST this.
  wall            the commonest short sound in a fight (263 of 543 calls in
                  the stage-4 smoke). A hex snap that measures like a wall tick
                  would be lost among them.

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:

  * Every voice is scheduled at t = 1.0 inside a 2.5s OfflineAudioContext,
    through `Sfx.buildChain` (bus 0.42 -> compressor -> makeup), on a synth
    built the way `render.py` builds one: `Object.create` of the Sfx prototype
    with render.py's xorshift NOISE, so the control and every candidate hear
    the same noise and two renders agree (checked: each candidate is rendered
    twice and must match to -120 dB -- Chromium 151 moves the last float bit
    when it sums oscillators, 6e-8 on rune-crack itself). `_noiseBuffer`'s
    Math.random moved one candidate from 0.269 to 0.486 peak (v66).
  * A 1.0s buffer renders NOTHING (v59). Nothing may sound before t = 1.0
    either -- checked, because that is what a broken currentTime proxy does.
  * AUDIBLE = the span from the first to the last 5 ms RMS window above 2% of
    the voice's own loudest 5 ms window (-34 dB). The stage-4 smoke's
    definition, so its published controls (rune-crack 450 ms, hit@11.6 80 ms)
    are reproduced here before anything new is quoted. A -20 dB span is
    printed beside it.
  * ENERGY CENTRE = the sum of t*x^2 over the sum of x^2, in ms after t = 1.0;
    LATE = (centre - audible start) / audible length. A struck voice is early
    (~0.2); a rising one is late (> 0.5).
  * ST-RMS = the loudest 50 ms RMS (5 ms hop): the short-term loudness proxy
    "quieter" is judged on, beside the raw peak.
  * REG = cosine similarity of the 1/3-octave band amplitudes (25 Hz-16 kHz)
    against a reference -- the echo's against the hit's (the literal reversal
    scores ~1 by construction), the cast's against rune-crack's -- as the
    MEDIAN over twelve noise draws, each against the reference on the same
    draw (one draw moved a register by up to 0.08).
  * NOISE DRAWS: the live game and `cinema_clip` fill the 0.6s noise buffer
    from Math.random, so anything built from noise is a different loudness in
    every session and every clip. Levels are therefore judged on the WORST of
    twelve xorshift draws, each against the control on the same draw. A
    narrow-band noise body moved one echo candidate x2.35 in short-term
    level; a sine body moves x1.06.
  * RISE = rise time of the 1 ms envelope from 10% to 90% of its max (the hex
    snap's "hard onset"); DIPS = dips of more than 3 dB in the 25 ms envelope
    on the way up to the peak (a single swell has none; re-strikes show up;
    5 ms is shorter than a period of the hit's 46 Hz floor and reads a pure
    rising sine as dips); RIP = the Hilbert envelope's RMS ripple in dB about
    its own 20 ms average (the hit itself: 3.2).

THE PICKS, on Chromium 151 (sc-corollary 710d3e4), and the reason each won:

  cast  1 BAR       audible 300 ms, peak 0.364 at 7 ms, register vs
                    rune-crack 0.35 (NOTE 0.40, GLINT 0.73, LINE 0.80 = out)
  echo  1 MIRROR    the hit's sine reversed and re-struck IN PHASE at its own
                    cycle starts: register vs the hit 0.98 (literal 1.00),
                    late 0.60, peak at 148 ms, st/hit 0.50-0.53 and pk/hit
                    0.44-0.57 over every noise draw. RESONANT (one q 8 noise
                    sweep, the obvious build) swung x2.35 across draws.
  hex   5 SNAP      audible 25 ms, rise < 1 ms, centroid 3.35 kHz; registers
                    wall 0.61 / echo 0.20 / rune-crack 0.41 (CRACK 0.69 on the
                    wall, GLINT 0.83 on rune-crack, KNOT a knock)

AND THE TOOLKIT'S BUGS ARE DESIGNED AROUND, NOT FIXED: `_burst` does not loop
its 0.6s noise buffer and `_tone` only decays (CLAUDE.md 4.5, open item 6). The
lab wraps `_burst` / `_sweep` on its synth and REFUSES any candidate with a
burst over 0.55s or a sweep over 0.58s, and refuses any candidate source that
names Math.random, rng or spawnFx.

Writes small wavs to 05-reference/v88/ at RAW level (not normalised, so the
files compare by ear the way the numbers compare). Refuses to write silence.
Touches no build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
SR = 48000
SECS = 2.5
T0 = 1.0

# ------------------------------------------------------------- THE CAST -----
# "a rune-chime, 0.3s" beside the picture's "the blade's edge lights with a
# rune line". A CHIME is struck and rings; 0.3s is its audible length under
# the declared definition. Rune-crack (a 6 kHz crack, a square falling
# 1800->300, a triad ringing 0.5s) is what it replaces and must not resemble.
CAST_CANDIDATES = [
    ("1 BAR",    "one struck inharmonic bar, free-bar modes 1 : 2.76 : 5.40"),
    ("2 LINE",   "two struck bars a fifth apart, 70 ms: the rune line running"),
    ("3 GLINT",  "a bright sweep lighting into a beating glass pair"),
    ("4 NOTE",   "harmonic 1:2:3 -- a musical note, the control on 'inharmonic'"),
]

CAST_VOICES_JS = r"""((S) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  const W = (t, o) => S._sweep(t, o);
  return [
  /* 1 -- BAR. One strike. The partials are a free bar's modes (1, 2.76,
     5.40), which is what makes a struck metal bar a CHIME rather than a note;
     a 20 ms tick at 5.2 kHz is the mallet. The body an octave under keeps it
     from reading thin in a hall of low thumps. */
  (t) => {
    B(t, { freq: 5200, q: 2.0, gain: 0.09, dur: 0.020, type:"bandpass" });
    [[1319, 1.00], [3640, 0.42], [7123, 0.16]].forEach(([fq, k]) =>
      T(t, { freq: fq, to: fq * 0.996, gain: 0.15 * k, dur: 0.51,
             type:"triangle" }));
    T(t, { freq: 659, to: 656, gain: 0.07, dur: 0.40, type:"sine" });
  },
  /* 2 -- LINE. Two strikes a fifth apart, the second 70 ms after the first:
     the rune line RUNNING along the edge, which is what the cast's picture
     draws. Each strike is the BAR's partials, quieter. */
  (t) => {
    [[0.00, 988, 1.00], [0.07, 1480, 0.85]].forEach(([d, f, g]) => {
      B(t + d, { freq: 4800, q: 2.2, gain: 0.07 * g, dur: 0.016,
                 type:"bandpass" });
      T(t + d, { freq: f, to: f * 0.997, gain: 0.14 * g, dur: 0.42,
                 type:"triangle" });
      T(t + d, { freq: f * 2.76, to: f * 2.76 * 0.997, gain: 0.045 * g,
                 dur: 0.25, type:"triangle" });
    });
  },
  /* 3 -- GLINT. A narrow sweep climbing 1.8 -> 6.4 kHz (the edge catching)
     into a glass pair 8 Hz apart that beats as it rings. */
  (t) => {
    W(t, { f0: 1800, f1: 6400, q: 3.0, gain: 0.12, dur: 0.14, atk: 0.05 });
    T(t + 0.05, { freq: 1760, to: 1754, gain: 0.10, dur: 0.60, type:"sine" });
    T(t + 0.05, { freq: 1768, to: 1762, gain: 0.10, dur: 0.60, type:"sine" });
    T(t + 0.05, { freq: 880, to: 878, gain: 0.06, dur: 0.46,
                  type:"triangle" });
  },
  /* 4 -- NOTE. Harmonic partials, 1 : 2 : 3 -- a pitched note rather than a
     struck object. The control on whether "chime" needs the inharmonic
     ratios at all. */
  (t) => {
    B(t, { freq: 4000, q: 1.5, gain: 0.07, dur: 0.020, type:"bandpass" });
    [[1, 1.00], [2, 0.45], [3, 0.22]].forEach(([r, k]) =>
      T(t, { freq: 784 * r, gain: 0.15 * k, dur: 0.53, type:"triangle" }));
  },
  ];
})"""

# ------------------------------------------------------------- THE ECHO -----
# "the sword's own strike voice, reversed (a rising "whoom"), quieter". The
# strike voice is `hit` (sc-corollary `if (kind === "hit")`):
#     w  = clamp((dmg || 10) / 45, 0.12, 1)
#     noise  bandpass 2600-1500w Hz, q 1.1, gain 0.16+0.20w, dur 0.06+0.06w
#     sine   190-90w -> 46 Hz,          gain 0.22+0.26w, dur 0.11+0.13w
# Reversed, the sine RISES 46 -> 190-90w while it SWELLS, the noise band swells
# in over the last 0.06+0.06w, and both END together where the strike began.
# Every candidate derives its numbers from those same formulas, so it can be
# rendered at any dmg -- that is how "should it scale with dmg" is measured.
#
# THE LITERAL REVERSAL CANNOT SHIP (see the docstring) -- every candidate is
# built synchronously from `_tone` / `_sweep`, and is measured against it.
ECHO_CANDIDATES = [
    ("1 MIRROR", "the hit's own sine run backwards (46 Hz rising to the hit's "
                 "pitch, swelling), re-struck IN PHASE at each of its own "
                 "cycles; the hit's noise band swells in to the same top"),
    ("2 WHOOM",  "MIRROR at 1.6x the length: a longer pass"),
    ("3 RESONANT", "the same rise as ONE resonant (q 8) noise band sweeping up "
                   "through the hit's pitch -- no re-strikes"),
    ("4 RESTRIKE", "the redflail precedent: four sine re-strikes climbing and "
                   "louder, NOT phase-locked"),
    ("5 AIR",    "a low-Q whoosh with no resonance: a rise with no pitch in it"),
]

ECHO_VOICES_JS = r"""((S, dmg) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  const W = (t, o) => S._sweep(t, o);
  const p = { dmg: dmg };
  /* THE HIT'S OWN WEIGHT AND NUMBERS, verbatim from `kind === "hit"`. `hw`
     and not `w`: inside the `ult` branch `w` is already the relic id. */
  const hw = clamp((p.dmg || 10) / 45, 0.12, 1);
  const tf = 190 - 90 * hw, tg = 0.22 + 0.26 * hw, td = 0.11 + 0.13 * hw;
  const nf = 2600 - 1500 * hw, ng = 0.16 + 0.20 * hw, nd = 0.06 + 0.06 * hw;
  /* THE REVERSED SINE, RE-STRUCK IN PHASE. Run backwards over `span`, the
     hit's sine is f(s) = 46 r^(s/span), r = tf/46, swelling to its peak at
     `span`. `_tone`'s gain only decays, so the swell is built out of short
     strikes -- and a strike placed at one of the chirp's own CYCLE STARTS
     begins at phase 0 where the chirp is at phase 0 and rides the same
     exponential pitch curve, so every strike is in phase with every other and
     they sum into ONE rising sine rather than a flutter. Cycle c starts at
     s_c = span / ln r * ln(1 + c ln r / (46 span)). Strikes run from `from`
     of the span (where the swell is still -34 dB x (1 - from) down) to the
     top, each `db`-scaled so the level climbs in a straight line in dB, as
     the hit's decay does run backwards. */
  const rise = (t, span, gain, dur, from, db) => {
    const r = tf / 46, L = Math.log(r);
    const c0 = Math.ceil(46 * span / L * (Math.pow(r, from) - 1));
    const c1 = Math.floor(46 * span / L * (r - 1));
    for (let c = c0; c <= c1; c++){
      const s = span / L * Math.log(1 + c * L / (46 * span));
      T(t + s, { freq: 46 * Math.pow(r, s / span),
                 to: 46 * Math.pow(r, (s + dur) / span),
                 gain: gain * Math.pow(10, -db * (1 - s / span) / 20),
                 dur: dur, type:"sine" });
    }
  };
  /* the hit's noise band, swelling in over the hit's own burst length and
     peaking on the same instant as the sine. `_sweep` peaks at 0.6 x dur. */
  const band = (t, span, sn, gain) =>
    W(t + span - sn, { f0: nf * 0.6, f1: nf * 1.25, q: 1.1, gain: gain,
                       dur: sn / 0.6, atk: sn, type:"bandpass" });
  return [
  /* 1 -- MIRROR. The hit, backwards, at the hit's own length: the sine's top
     lands one strike-length (td) after the echo lands. */
  (t) => { rise(t, td, tg * 0.30, 0.05, 0.45, 34); band(t, td, nd, ng * 0.45); },
  /* 2 -- WHOOM. MIRROR at 1.6x the span, so the rise is heard as a pass. */
  (t) => { rise(t, 1.6 * td, tg * 0.26, 0.06, 0.45, 34);
           band(t, 1.6 * td, 1.6 * nd, ng * 0.45); },
  /* 3 -- RESONANT. One `_sweep`: bandpass at q 8 RESONATES, so a noise band
     sweeping up through the hit's pitch carries that pitch. f1 is set so the
     centre is at tf at the sweep's peak (0.6 x dur). */
  (t) => { W(t, { f0: tf * 0.55, f1: tf * 1.49, q: 8, gain: tg * 18,
                  dur: td / 0.6, atk: td, type:"bandpass" });
           band(t, td, nd, ng * 0.40); },
  /* 4 -- RESTRIKE. `_tone`'s gain only decays, so redflail builds a swell
     from overlapping events each louder than the last. Four strikes on the
     same pitch curve, 0.2 td apart -- not at cycle starts. */
  (t) => { [0.40, 0.60, 0.80, 1.00].forEach((u) => {
             const s = u * td;
             T(t + s, { freq: 46 * Math.pow(tf / 46, s / td),
                        to: 46 * Math.pow(tf / 46, (s + 0.10) / td),
                        gain: tg * 0.40 * Math.pow(10, -26 * (1 - u) / 20),
                        dur: 0.10, type:"sine" }); });
           band(t, td, nd, ng * 0.45); },
  /* 5 -- AIR. MIRROR's timing as a plain low-Q whoosh: the control on
     whether the pitch is what keeps it in the hit's register. */
  (t) => { W(t, { f0: 80, f1: 700, q: 0.7, gain: tg * 2.0, dur: td / 0.6,
                  atk: td, type:"lowpass" });
           band(t, td, nd, ng * 0.45); },
  ];
})"""

# -------------------------------------------------------------- THE HEX -----
# "the hex -- its snap". No hex voice exists anywhere in the build, and v79
# Spellbreaker ("hex's own snap") and v75 Oracle ("a hex snap") name the same
# sound -- so this is the RUNIC SCHOOL's snap, its own `kind`, and not an
# Axiom sub-voice. It fires on the echo's hex, on the same frame the echo's
# rising voice STARTS, so it has to be short, hard at the front, and clear of
# both the hit's register (46-190 Hz + ~2.2 kHz noise) and the wall tick.
# LEVEL-MATCHED: each candidate's gains CENTRE it, in dB, inside the level
# window the rule sets (3x the wall tick to 1x the hit, on its worst noise
# draw each way), so the pick is made on character and not on which one
# happened to be loudest.
HEX_CANDIDATES = [
    ("1 GLINT", "a bright bandpass click with a falling triangle glint"),
    ("2 CRACK", "a dry highpass crack over a short falling square"),
    ("3 KNOT",  "a mid click on a short low knock -- the thickest"),
    ("4 SEAL",  "two ticks 18 ms apart, low then high, and a glint: a latch"),
    ("5 SNAP",  "a finger-snap band (2.6 kHz, 22 ms) on a small body, with a "
                "high ping held nearly level"),
]

HEX_VOICES_JS = r"""((S) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  return [
  (t) => {
    B(t, { freq: 4200, q: 1.6, gain: 0.34, dur: 0.030, type:"bandpass" });
    T(t, { freq: 1600, to: 640, gain: 0.15, dur: 0.07, type:"triangle" });
  },
  (t) => {
    B(t, { freq: 5200, q: 0.9, gain: 0.152, dur: 0.025, type:"highpass" });
    T(t, { freq: 900, to: 240, gain: 0.076, dur: 0.05, type:"square" });
  },
  (t) => {
    B(t, { freq: 1800, q: 1.4, gain: 0.26, dur: 0.035, type:"bandpass" });
    T(t, { freq: 280, to: 110, gain: 0.20, dur: 0.07, type:"sine" });
  },
  (t) => {
    B(t, { freq: 3200, q: 2.0, gain: 0.40, dur: 0.020, type:"bandpass" });
    B(t + 0.018, { freq: 5600, q: 2.0, gain: 0.36, dur: 0.020,
                   type:"bandpass" });
    T(t + 0.018, { freq: 2400, to: 1400, gain: 0.14, dur: 0.05,
                   type:"triangle" });
  },
  /* 5 -- SNAP. The band a finger snap lives in (~2-3 kHz), 22 ms, over a
     short 1.3 kHz body so it has a front AND a thickness; the ping on top is
     a triangle held almost level (3100 -> 2500), which is what makes it a
     rune's snap rather than a stick's. The bands are WIDE (q 1.2 / 1.0) and
     the ping carries a share of the level, because a narrow noise band is a
     different loudness on every noise draw (q 2.2 moved it x1.43). */
  (t) => {
    B(t, { freq: 2600, q: 1.2, gain: 0.38, dur: 0.022, type:"bandpass" });
    B(t, { freq: 1300, q: 1.0, gain: 0.15, dur: 0.030, type:"bandpass" });
    T(t, { freq: 3100, to: 2500, gain: 0.138, dur: 0.045, type:"triangle" });
  },
  ];
})"""

SOURCES = {"cast": CAST_VOICES_JS, "echo": ECHO_VOICES_JS, "hex": HEX_VOICES_JS}
for _k, _src in SOURCES.items():
    _bad = re.findall(r"Math\.random|\brng\b|spawnFx", _src)
    if _bad:
        raise SystemExit(f"REFUSING: the {_k} candidates name {_bad} -- a "
                         "voice must draw no random number (a render must "
                         "reproduce, and presentation must never touch rng).")

# ------------------------------------------------------------- THE RENDER ---
# `evs` is a list of events, each rendered at its own time on ONE synth:
#   ["play", at, kind, p]            SFX.play(kind, p) with currentTime = at
#   ["cand", at, voice, i, dmg]      candidate i of SOURCES[voice], at `at`
#   ["literal", at, kind, p]         SFX.play rendered DRY, samples reversed,
#                                    played through the chain from `at` (lab
#                                    reference only -- async by construction)
RENDER_JS = r"""async ([evs, secs, srcs, seed]) => {
  const OC = window.OfflineAudioContext, sr = 48000;
  const proto = Object.getPrototypeOf(AC.SFX);
  /* render.py's xorshift, verbatim, from render.py's seed unless another is
     asked for: the live game and `cinema_clip` fill this buffer from
     Math.random, so a voice is also measured across OTHER noise draws. */
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
    /* the toolkit's two traps, checked on every call a candidate makes */
    const log = { burst: [], sweep: [], tone: 0 };
    S._burst = function(t, o, d){ log.burst.push(o.dur); return proto._burst.call(this, t, o, d); };
    S._sweep = function(t, o, d){ log.sweep.push(o.dur); return proto._sweep.call(this, t, o, d); };
    S._tone  = function(t, o, d){ log.tone++; return proto._tone.call(this, t, o, d); };
    return { S, log, at: (x) => { cursor = x; } };
  };
  const oc = new OC(1, Math.round(sr * secs), sr);
  const Y = synth(oc, true);
  for (const e of evs){
    if (e[0] === "play"){ Y.at(e[1]); Y.S.play(e[2], e[3]); }
    else if (e[0] === "cand"){ Y.at(e[1]);
      const V = eval(srcs[e[2]])(Y.S, e[4]); V[e[3]](e[1]); }
    else if (e[0] === "literal"){
      const dc = new OC(1, Math.round(sr * secs), sr), Z = synth(dc, false);
      Z.at(1.0); Z.S.play(e[2], e[3]);
      const dry = (await dc.startRendering()).getChannelData(0);
      let a = 0, b = dry.length - 1; const TH = 1e-5;
      while (a < dry.length && Math.abs(dry[a]) < TH) a++;
      while (b > a && Math.abs(dry[b]) < TH) b--;
      const seg = dry.slice(a, b + 1).reverse();
      const rb = oc.createBuffer(1, seg.length, sr); rb.copyToChannel(seg, 0);
      const src = oc.createBufferSource(); src.buffer = rb;
      src.connect(Y.S.bus); src.start(e[1]);
    }
  }
  const buf = await oc.startRendering();
  const d = buf.getChannelData(0);
  let h = 2166136261 >>> 0;              /* FNV-1a over the float bits */
  const u8 = new Uint8Array(d.buffer, d.byteOffset, d.byteLength);
  for (let i = 0; i < u8.length; i++){ h ^= u8[i]; h = Math.imul(h, 16777619) >>> 0; }
  return { pcm: Array.from(d), hash: h.toString(16), log: Y.log };
}"""

# What the echo's damage actually is, measured: every landed echo's queued
# dmg, recorded where `tickEcho` hands it to `hurt`, Axiom on both sides
# against every other relic. The wraps pass straight through.
DIST_JS = r"""([seeds]) => {
  const P = AC.Match.prototype, DT = AC.CONFIG.physics.dt;
  const oTick = P.tickEcho, oHurt = P.hurt;
  let inEcho = 0, depth = 0; const rec = [];
  P.tickEcho = function(dt){ inEcho++; try { return oTick.call(this, dt); } finally { inEcho--; } };
  P.hurt = function(tgt, dmg, src){
    if (inEcho && depth === 0 && src && src.w && src.w.id === "axiom") rec.push(dmg);
    depth++; try { return oHurt.apply(this, arguments); } finally { depth--; } };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "axiom");
  let landed = 0, fights = 0;
  try {
    for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
      const m = side ? new AC.Match(fid, "axiom", sd) : new AC.Match("axiom", fid, sd);
      const ax = side ? m.b : m.a; let steps = 0;
      while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
      fights++; if (ax.echoTally) landed += ax.echoTally.landed;
    }
  } finally { P.tickEcho = oTick; P.hurt = oHurt; }
  return { rec, landed, fights };
}"""


# ------------------------------------------------------------ MEASURING ----
def _np():
    import numpy as np
    return np


def voice(pcm):
    np = _np()
    d = np.asarray(pcm, dtype=np.float64)
    i0 = int(round(SR * T0))
    pre = float(np.abs(d[:i0]).max()) if i0 else 0.0
    return d, d[i0:], pre


def env(x, win_ms, hop_ms=None):
    np = _np()
    W = int(SR * win_ms / 1000); H = int(SR * (hop_ms or win_ms) / 1000)
    n = max(0, (len(x) - W) // H + 1)
    return np.array([np.sqrt(np.mean(x[k * H:k * H + W] ** 2))
                     for k in range(n)]), H


BANDS = None


def bands(x):
    """1/3-octave band amplitudes, 25 Hz - 16 kHz, of a voice segment."""
    np = _np()
    global BANDS
    if BANDS is None:
        BANDS = [25 * 2 ** (k / 3) for k in range(0, 29)]
    F = np.fft.rfft(x); P = np.abs(F) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    out = []
    for fc in BANDS:
        lo, hi = fc / 2 ** (1 / 6), fc * 2 ** (1 / 6)
        out.append(np.sqrt(P[(fr >= lo) & (fr < hi)].sum()))
    return np.array(out)


def cos(a, b):
    np = _np()
    return float(np.dot(a, b) / ((np.linalg.norm(a) * np.linalg.norm(b)) or 1))


def mreg(A, B):
    """A register as the MEDIAN over the noise draws, each draw of A against
    the same draw of B. One draw is one sample: on render.py's draw CRACK read
    0.65 against the wall tick and SNAP 0.69, and over twelve draws CRACK is
    0.69 [0.65-0.71] and SNAP 0.61 [0.54-0.69] -- the single draw had them the
    wrong way round."""
    np = _np()
    return float(np.median([cos(a["bands"], b["bands"]) for a, b in zip(A, B)]))


def measure(pcm):
    np = _np()
    _, x, pre = voice(pcm)
    peak = float(np.abs(x).max())
    if peak < 1e-6:
        return dict(peak=0.0, silent=True, pre=pre)
    e5, _ = env(x, 5)
    top = e5.max()
    on = np.nonzero(e5 > top * 0.02)[0]
    a0, a1 = int(on[0]), int(on[-1])
    aud = (a1 - a0 + 1) * 5.0
    on20 = np.nonzero(e5 > top * 0.10)[0]
    aud20 = (int(on20[-1]) - int(on20[0]) + 1) * 5.0
    pk_ms = float(np.argmax(np.abs(x)) / SR * 1000)
    e2 = x ** 2
    ec = float((e2 * np.arange(len(x))).sum() / e2.sum() / SR * 1000)
    late = (ec - a0 * 5.0) / aud if aud else 0.0
    st, _ = env(x, 50, 5)
    aud_rms = float(np.sqrt(np.mean(x[a0 * 240:(a1 + 1) * 240] ** 2)))
    e1, _ = env(x, 1)
    m1 = e1.max(); i10 = int(np.argmax(e1 > 0.1 * m1)); i90 = int(np.argmax(e1 > 0.9 * m1))
    rise = float(i90 - i10)
    # dips on the way up: a drop of > 3 dB below the running max before the
    # peak, on a 25 ms RMS (5 ms hop) -- a 5 ms window is shorter than one
    # period of the hit's 46 Hz floor and reads a pure rising sine as dips.
    e25, _ = env(x, 25, 5)
    ip = int(np.argmax(e25)); run = 0.0; dips = 0; indip = False
    for v in e25[max(0, a0 - 4):ip + 1]:
        run = max(run, v)
        if run > e25.max() * 0.05 and v < run * 0.708:
            if not indip: dips += 1
            indip = True
        else:
            indip = False
    # NO WINDOW on the spectrum: the segment starts AT the onset, so a Hann
    # window zeroes the attack (it moved the hit's <120 Hz share 52% -> 9%).
    # The voice rises from and decays to silence, so there is no edge.
    F = np.fft.rfft(x); P = np.abs(F) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / SR); tot = P.sum() or 1.0
    # RIPPLE: the Hilbert envelope's RMS deviation, in dB, from its own 20 ms
    # moving average, wherever it is within 20 dB of its max. A single smooth
    # swell is low; beating re-strikes and narrow noise are high. The hit's
    # own is the reference.
    N = len(x); Xf = np.fft.fft(x); h = np.zeros(N); h[0] = 1
    h[1:(N + 1) // 2] = 2
    if N % 2 == 0: h[N // 2] = 1
    he = np.abs(np.fft.ifft(Xf * h)); hdb = 20 * np.log10(np.maximum(he, 1e-9))
    ma = np.convolve(hdb, np.ones(960) / 960, mode="same"); sel = he > he.max() * 0.1
    rip = float(np.sqrt(np.mean((hdb[sel] - ma[sel]) ** 2)))
    return dict(peak=peak, pk_ms=pk_ms, a0=a0 * 5.0, aud=aud, aud20=aud20,
                ec=ec, late=late, st=float(st.max()), rms=aud_rms, rise=rise,
                dips=dips, rip=rip, low=float(P[fr < 120].sum() / tot),
                cen=float((P * fr).sum() / tot), bands=bands(x), pre=pre,
                silent=False)


def write_wav(path, pcm, pad=0.08):
    """Raw level -- NOT normalised -- trimmed to the voice and a little air."""
    np = _np()
    d, x, _ = voice(pcm)
    top = float(np.abs(x).max())
    if top < 1e-6:
        raise SystemExit(
            f"REFUSING TO WRITE {path.name} -- it rendered SILENCE.\n"
            "  That is v42's defect exactly: `SFX.play` returns on its first\n"
            "  line headless and wraps its body in try/catch, so a silent\n"
            "  voice passes every other check in this repo.")
    nz = np.nonzero(np.abs(x) > top * 1e-3)[0]
    i0 = int(round(SR * T0))
    a = max(0, i0 + int(nz[0]) - int(pad * SR))
    b = min(len(d), i0 + int(nz[-1]) + int(pad * SR))
    seg = np.clip(d[a:b], -1, 1)
    w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((seg * 32767).astype("<i2").tobytes())
    w.close()
    return path.stat().st_size




# --------------------------------------------------------------- PICKING ---
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v80 §4 turned into a number; the
# tiebreak is said. A rule no candidate passes exits 1 rather than picking
# the least bad.
FAILED: list = []

CAST_RULE = ("audible 250-350 ms (the spec's 0.3s, by the declared definition);"
             " register vs rune-crack <= 0.80 (clearly not it); peak >= 0.25 "
             "(heard in a fight). Tiebreak: closest to 300 ms in 20 ms steps, "
             "then furthest from rune-crack.")
ECHO_RULE = ("late >= 0.55 (rising); over all noise draws pk/hit <= 0.75 and "
             "st/hit <= 0.75 (quieter) and st/hit >= 0.35 (still heard); "
             "register vs hit >= 0.85 (the sword's own voice); no dips (one "
             "swell); peak 100-165 ms (topping as the drawn 0.15 s ghost sweep "
             "ends). Tiebreak: closest register, then the tightest level "
             "across noise draws.")
# THE HEX RULE WAS WIDENED ONCE, AND THIS IS WHY. Its first cut (audible,
# onset, level; tiebreak "most distinct") picked KNOT -- a 366 Hz-centroid
# KNOCK whose register overlaps the echo's by 0.54, on the very frame the echo
# starts. "Snap" names a bright sound, and this one always lands on top of the
# echo's rise, so two gates were added: centroid >= 1 kHz and register vs the
# picked echo <= 0.40. Recorded rather than hidden: the rule is the pick's.
HEX_RULE = ("audible <= 120 ms; rise <= 2 ms and peak in the first 10 ms (a "
            "hard onset); peak between 3x the wall tick's and the hit's "
            "(heard, not louder than a blow); centroid >= 1 kHz (a snap, not "
            "a knock); register vs the picked echo <= 0.40 (it lands on the "
            "echo's frame); the level gates hold on EVERY noise draw, each "
            "against the hit and the wall on that draw. Tiebreak: the most "
            "distinct -- lowest of its registers vs the wall tick, the picked "
            "echo and rune-crack, to 0.05 -- then the furthest centroid from "
            "the wall tick's, in octaves (the wall is the commonest sound in a "
            "fight: 263 of 543 calls).")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the fewest failures is "
              "shown, and the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def pick_cast(rows):
    for M in rows:
        why = []
        if not 250 <= M["aud"] <= 350: why.append(f"audible {M['aud']:.0f} ms, not ~300")
        if M["rc_reg"] > 0.80: why.append(f"register vs rune-crack {M['rc_reg']:.2f} > 0.80")
        if M["peak"] < 0.25: why.append(f"peak {M['peak']:.3f} < 0.25")
        M["why"] = why
    ok, fb = _gate(rows, "cast")
    if ok is None: return fb
    return min(ok, key=lambda i: (abs(rows[i]["aud"] - 300) // 20, rows[i]["rc_reg"]))


def pick_echo(rows):
    for M in rows:
        why = []
        if M["late"] < 0.55: why.append(f"energy centre early (late {M['late']:.2f})")
        if M["pk_hi"] > 0.75: why.append(f"pk/hit up to {M['pk_hi']:.2f} > 0.75")
        if M["st_hi"] > 0.75: why.append(f"st/hit up to {M['st_hi']:.2f} > 0.75")
        if M["st_lo"] < 0.35: why.append(f"st/hit down to {M['st_lo']:.2f} < 0.35")
        if M["reg"] < 0.85: why.append(f"register vs hit {M['reg']:.2f} < 0.85")
        if M["dips"] > 0: why.append(f"{M['dips']} dips on the rise")
        if not 100 <= M["pk_ms"] <= 165: why.append(f"peak at {M['pk_ms']:.0f} ms, not 100-165")
        M["why"] = why
    ok, fb = _gate(rows, "echo")
    if ok is None: return fb
    return max(ok, key=lambda i: (round(rows[i]["reg"], 2), -rows[i]["st_x"]))


def pick_hex(rows, wall, hit):
    for M in rows:
        why = []
        if M["aud"] > 120: why.append(f"audible {M['aud']:.0f} ms > 120")
        if M["rise"] > 2.0: why.append(f"rise {M['rise']:.0f} ms > 2")
        if M["pk_ms"] > 10: why.append(f"peak at {M['pk_ms']:.0f} ms, not the front")
        if M["pw_lo"] < 3: why.append(f"peak down to {M['pw_lo']:.1f}x the wall's < 3x")
        if M["ph_hi"] > 1: why.append(f"peak up to {M['ph_hi']:.2f}x the hit's > 1")
        if M["cen"] < 1000: why.append(f"centroid {M['cen']:.0f} Hz < 1 kHz (a knock)")
        if M["echo_reg"] > 0.40: why.append(f"register vs the echo {M['echo_reg']:.2f} > 0.40")
        M["why"] = why
    ok, fb = _gate(rows, "hex")
    if ok is None: return fb
    import math
    return min(ok, key=lambda i: (round(max(rows[i]["wall_reg"], rows[i]["echo_reg"],
                                            rows[i]["rc_reg"]) / 0.05),
                                  -abs(math.log2(rows[i]["cen"] / wall["cen"]))))


def same(r1, r2, what):
    """Two renders of one candidate must agree to -120 dB. Not bit-for-bit:
    Chromium 151 sums several oscillators in an order that moves the last
    float32 bit (measured: 6e-8 on rune-crack itself, 0 on the hit). A voice
    on Math.random noise differs by ~0.1, so this still fails when it should."""
    np = _np()
    d = float(np.abs(np.asarray(r1["pcm"]) - np.asarray(r2["pcm"])).max())
    if d > 1e-6:
        raise SystemExit(f"{what} does not reproduce: two renders differ by "
                         f"{d:.2e} -- a voice drawing a random number?")
    return d


def row(name, M, extra=""):
    return (f"  {name:<12}{M['peak']:>7.3f}{M['pk_ms']:>6.0f}{M['aud']:>6.0f}"
            f"{M['aud20']:>6.0f}{M['ec']:>6.0f}{M['late']:>6.2f}{M['st']:>7.3f}"
            f"{M['rise']:>5.0f}{M['dips']:>5d}{M['rip']:>6.1f}{M['low']:>7.1%}"
            f"{M['cen']:>7.0f}{extra}")


HEAD = (f"  {'voice':<12}{'peak':>7}{'pk@':>6}{'aud':>6}{'-20dB':>6}"
        f"{'Ectr':>6}{'late':>6}{'strms':>7}{'rise':>5}{'dips':>5}{'rip':>6}"
        f"{'<120':>7}{'cen Hz':>7}")

# render.py's seed first, then eleven other draws: the live game and
# cinema_clip fill the noise buffer from Math.random, so a noise-built voice
# is a different level in every session and every clip.
NOISE_SEEDS = [0x9e3779b9] + [(0x2545F491 * (k + 7)) & 0xffffffff or 1
                              for k in range(11)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corollary.html")
    ap.add_argument("--out", default="../05-reference/v88")
    ap.add_argument("--dmg", type=float, default=11.6,
                    help="the echo's damage for the main table (v88: 22.4 / "
                         "1.93 landed = 11.6, the mean echo)")
    ap.add_argument("--dist-seeds", type=int, default=2,
                    help="fight seeds per pairing for the echo-dmg "
                         "distribution (0 skips it: fixed 3/6/11.6/20/30)")
    ap.add_argument("--seed0", type=int, default=91001)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "dmg": a.dmg,
           "rules": {"cast": CAST_RULE, "echo": ECHO_RULE, "hex": HEX_RULE}}
    print(f"\nCOROLLARY -- THE THREE VOICES   game {gp.name}")
    print("  aud   = AUDIBLE: first..last 5 ms RMS window above 2% (-34 dB) of "
          "the voice's own loudest 5 ms window, ms\n  -20dB = the same at 10%;"
          " pk@ = sample peak, ms after onset; Ectr = energy centre, ms\n  late"
          "  = (Ectr - audible start) / audible  (struck ~0.15, rising > 0.5)\n"
          "  strms = loudest 50 ms RMS; rise = 10->90% of the 1 ms envelope, "
          "ms; dips = >3 dB dips of the 25 ms\n          envelope on the way "
          "up; rip = Hilbert-envelope ripple, dB RMS about its 20 ms average\n"
          "  every render at t = 1.0 in a 2.5 s OfflineAudioContext, through "
          "Sfx.buildChain, on render.py's xorshift noise\n  unless a noise "
          f"draw is named ({len(NOISE_SEEDS)} draws for the spreads).")

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}\n")
        rec["chromium"] = ua

        def R(evs, seed=None):
            r = page.evaluate(RENDER_JS, [evs, SECS, SOURCES, seed])
            assert not errors, errors[:3]
            for d_ in r["log"]["burst"]:
                if d_ > 0.55:
                    raise SystemExit(f"REFUSING: a _burst of {d_}s (> 0.55) in {evs}")
            for d_ in r["log"]["sweep"]:
                if d_ > 0.58:
                    raise SystemExit(f"REFUSING: a _sweep of {d_}s (> 0.58) in {evs}")
            return r

        def M_(evs, seed=None):
            r = R(evs, seed)
            M = measure(r["pcm"])
            if M["silent"]:
                raise SystemExit(f"SILENT render: {evs}")
            if M["pre"] > 1e-6:
                raise SystemExit(f"sound BEFORE t=1.0 ({M['pre']:.2e}) in {evs}")
            M["calls"] = len(r["log"]["burst"]) + len(r["log"]["sweep"]) + r["log"]["tone"]
            return r, M

        def draws(evs):
            return [M_(evs, sd)[1] for sd in NOISE_SEEDS]

        # ---- CONTROLS, reproduced before anything new is quoted -------------
        print("CONTROLS -- the stage-4 smoke published rune-crack 0.608 / 450 ms,"
              " hit@11.6 0.443 / 80 ms / Ectr 15,\n  literal reversal @11.6 peak"
              " at 168 ms. They must come back, or nothing below is quoted.")
        print(HEAD)
        ctl = {}
        hk = f"hit@{a.dmg:g}"
        for name, evs in (
            ("rune-crack", [["play", T0, "ult", {"w": "axiom"}]]),
            ("starwarden", [["play", T0, "ult", {"w": "starwarden"}]]),
            (hk, [["play", T0, "hit", {"dmg": a.dmg, "crit": False}]]),
            ("literal", [["literal", T0, "hit", {"dmg": a.dmg, "crit": False}]]),
            ("hit@7.42", [["play", T0, "hit", {"dmg": 7.42, "crit": False}]]),
            ("wall", [["play", T0, "wall", {}]]),
            ("aegis n1", [["play", T0, "aegis", {"n": 1}]]),
        ):
            r, M = M_(evs)
            ctl[name] = (r, M)
            print(row(name, M))
        hitM, rcM, wallM, litM = (ctl[hk][1], ctl["rune-crack"][1],
                                  ctl["wall"][1], ctl["literal"][1])
        repro = [("rune-crack peak", rcM["peak"], 0.608, 0.01),
                 ("rune-crack audible", rcM["aud"], 450, 10)]
        if a.dmg == 11.6:
            repro += [("hit@11.6 peak", hitM["peak"], 0.443, 0.01),
                      ("hit@11.6 audible", hitM["aud"], 80, 10),
                      ("hit@11.6 Ectr", hitM["ec"], 15, 3),
                      ("literal@11.6 peak at", litM["pk_ms"], 168, 5)]
        bad = [f"{n}: {v:.3f} vs published {p_}" for (n, v, p_, tol) in repro
               if abs(v - p_) > tol]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
              f"PASS  all {len(repro)} published control numbers come back"))
        if bad:
            raise SystemExit("the controls do not reproduce -- nothing new "
                             "is quoted on this runtime")
        HD = draws([["play", T0, "hit", {"dmg": a.dmg, "crit": False}]])
        RD = draws([["play", T0, "ult", {"w": "axiom"}]])
        WD = draws([["play", T0, "wall", {}]])
        print(f"  the hit across {len(NOISE_SEEDS)} noise draws: peak "
              f"{min(m['peak'] for m in HD):.3f}-{max(m['peak'] for m in HD):.3f}"
              f", strms {min(m['st'] for m in HD):.3f}-{max(m['st'] for m in HD):.3f}")
        print(f"  literal reversal vs the hit: register {cos(litM['bands'], hitM['bands']):.3f}"
              " -- the ceiling a built reversal is measured against")
        rec["controls"] = {k: {kk: vv for kk, vv in v[1].items() if kk != "bands"}
                           for k, v in ctl.items()}
        sizes = {}

        def wav(name, pcm):
            sizes[name] = write_wav(out / name, pcm)

        wav("corollary-cast-0-runecrack.wav", ctl["rune-crack"][0]["pcm"])
        wav("corollary-echo-0-hit.wav", ctl[hk][0]["pcm"])
        wav("corollary-echo-0-literal.wav", ctl["literal"][0]["pcm"])
        wav("corollary-hex-0-wall.wav", ctl["wall"][0]["pcm"])

        # ---- THE CAST ------------------------------------------------------
        print("\nCAST -- 'a rune-chime, 0.3s'.  rc reg = register vs rune-crack;"
              " pk x = peak spread across noise draws")
        print(HEAD + f"{'rc reg':>7}{'pk x':>6}")
        cast = []
        for i, (name, blurb) in enumerate(CAST_CANDIDATES):
            r, M = M_([["cand", T0, "cast", i, 0]])
            same(r, R([["cand", T0, "cast", i, 0]]), f"cast {i + 1}")
            Ds = draws([["cand", T0, "cast", i, 0]])
            M["pk_x"] = max(d["peak"] for d in Ds) / min(d["peak"] for d in Ds)
            M["rc_reg"] = mreg(Ds, RD)
            cast.append(M)
            print(row(name, M, f"{M['rc_reg']:>7.2f}{M['pk_x']:>6.2f}   {blurb}"))
            wav(f"corollary-cast-{i + 1}.wav", r["pcm"])
        print(f"  RULE  {CAST_RULE}")
        ci = pick_cast(cast)
        for i, M in enumerate(cast):
            if M["why"]:
                print(f"    {CAST_CANDIDATES[i][0]:<10} out: {'; '.join(M['why'])}")
        print(f"  PICK  {CAST_CANDIDATES[ci][0]}")

        # ---- THE ECHO ------------------------------------------------------
        print(f"\nECHO @ dmg {a.dmg:g} -- 'the sword's own strike voice, reversed "
              "(a rising whoom), quieter'")
        print("  reg = register vs the hit (median over the draws); pk/hit and "
              "st/hit are against the hit"
              " at the SAME dmg on the SAME noise draw,\n  as min-max over "
              f"{len(NOISE_SEEDS)} draws; st x = that spread as a factor")
        print(HEAD + f"{'reg':>6}{'pk/hit':>11}{'st/hit':>11}{'st x':>6}")
        print(row(hk, hitM, f"{1:>6.2f}"))
        print(row("literal", litM, f"{cos(litM['bands'], hitM['bands']):>6.2f}"
                  f"{litM['peak'] / hitM['peak']:>11.2f}{litM['st'] / hitM['st']:>11.2f}"))
        echo = []
        for i, (name, blurb) in enumerate(ECHO_CANDIDATES):
            ev = [["cand", T0, "echo", i, a.dmg]]
            r, M = M_(ev)
            same(r, R(ev), f"echo {i + 1}")
            Ds = draws(ev)
            pk = [d["peak"] / h["peak"] for d, h in zip(Ds, HD)]
            st = [d["st"] / h["st"] for d, h in zip(Ds, HD)]
            M.update(pk_lo=min(pk), pk_hi=max(pk), st_lo=min(st), st_hi=max(st),
                     st_x=max(st) / min(st), reg=mreg(Ds, HD))
            M["_draws"] = Ds
            echo.append(M)
            print(row(name, M, f"{M['reg']:>6.2f}{M['pk_lo']:>6.2f}-{M['pk_hi']:.2f}"
                      f"{M['st_lo']:>6.2f}-{M['st_hi']:.2f}{M['st_x']:>6.2f}"))
            wav(f"corollary-echo-{i + 1}.wav", r["pcm"])
        for i, (name, blurb) in enumerate(ECHO_CANDIDATES):
            print(f"    {name:<11} {blurb}  [{echo[i]['calls']} synth calls]")
        print(f"  RULE  {ECHO_RULE}")
        ei = pick_echo(echo)
        for i, M in enumerate(echo):
            if M["why"]:
                print(f"    {ECHO_CANDIDATES[i][0]:<10} out: {'; '.join(M['why'])}")
        print(f"  PICK  {ECHO_CANDIDATES[ei][0]}")

        # ---- THE HEX -------------------------------------------------------
        print("\nHEX -- 'its snap'.  registers vs the wall tick / the picked echo "
              "/ rune-crack; pk x = peak spread across draws;\n  /hit = its "
              "peak over the hit's on the WORST draw; /wall = over the wall "
              "tick's, the worst draw")
        print(HEAD + f"{'wall':>6}{'echo':>6}{'rc':>6}{'pk x':>6}{'/hit':>6}{'/wall':>6}")
        hexr = []
        for i, (name, blurb) in enumerate(HEX_CANDIDATES):
            ev = [["cand", T0, "hex", i, 0]]
            r, M = M_(ev)
            same(r, R(ev), f"hex {i + 1}")
            Ds = draws(ev)
            M["pk_x"] = max(d["peak"] for d in Ds) / min(d["peak"] for d in Ds)
            M["ph_hi"] = max(d["peak"] / h["peak"] for d, h in zip(Ds, HD))
            M["pw_lo"] = min(d["peak"] / w_["peak"] for d, w_ in zip(Ds, WD))
            M["wall_reg"] = mreg(Ds, WD)
            M["echo_reg"] = mreg(Ds, echo[ei]["_draws"])
            M["rc_reg"] = mreg(Ds, RD)
            hexr.append(M)
            print(row(name, M, f"{M['wall_reg']:>6.2f}{M['echo_reg']:>6.2f}"
                      f"{M['rc_reg']:>6.2f}{M['pk_x']:>6.2f}{M['ph_hi']:>6.2f}"
                      f"{M['pw_lo']:>6.1f}   {blurb}"))
            wav(f"corollary-hex-{i + 1}.wav", r["pcm"])
        print(row("wall", wallM, f"{1:>6.2f}{mreg(WD, echo[ei]['_draws']):>6.2f}"
                  f"{mreg(WD, RD):>6.2f}"))
        print(row("aegis n1", ctl["aegis n1"][1]))
        print(f"  RULE  {HEX_RULE}")
        hi = pick_hex(hexr, wallM, hitM)
        for i, M in enumerate(hexr):
            if M["why"]:
                print(f"    {HEX_CANDIDATES[i][0]:<10} out: {'; '.join(M['why'])}")
        print(f"  PICK  {HEX_CANDIDATES[hi][0]}")

        # ---- THE PICKS TOGETHER, as tickEcho will fire them -----------------
        # the blow's hit at 0; 0.5 s later the echo voice AND the snap on ONE
        # frame (hurt, then apply("hex")). Does the snap stay a snap on the
        # whoom's quiet start, and does the whoom still top out late?
        print("\nLAYERED -- the blow's hit at 0, then the picked echo + snap on "
              "one frame at +0.5 s, as tickEcho fires them")
        lay = [["play", T0, "hit", {"dmg": a.dmg, "crit": False}],
               ["cand", T0 + 0.5, "echo", ei, a.dmg],
               ["cand", T0 + 0.5, "hex", hi, 0]]
        rl = R(lay)
        x = voice(rl["pcm"])[1][int(0.5 * SR):]
        xe = voice(R([["cand", T0, "echo", ei, a.dmg]])["pcm"])[1]
        e25l, _ = env(x, 25, 5)
        e25e, _ = env(xe, 25, 5)
        e1l, _ = env(x, 1)
        snap = float(e1l[:12].max())
        at_l = int(np.argmax(e25l[8:]) + 8) * 5
        at_e = int(np.argmax(e25e)) * 5
        pk_l = float(np.abs(x[int(0.04 * SR):]).max())
        print(f"  snap 1 ms peak (first 12 ms) {snap:.3f}; the echo's own sample "
              f"peak after 40 ms {pk_l:.3f}  -> snap/echo {snap / pk_l:.2f}")
        print(f"  the echo's 25 ms envelope tops at +{at_l} ms layered, +{at_e} "
              "ms alone")
        wav("corollary-echo-pick-layered.wav", rl["pcm"])
        rec["layered"] = dict(snap=snap, echo_pk=pk_l, top_layered_ms=at_l,
                              top_alone_ms=at_e)

        # ---- SHOULD THE ECHO SCALE WITH DMG? -------------------------------
        if a.dist_seeds > 0:
            seeds = [a.seed0 + k for k in range(a.dist_seeds)]
            D = page.evaluate(DIST_JS, [seeds])
            assert not errors, errors[:3]
            dm = np.array(D["rec"], dtype=float)
            print(f"\nTHE ECHO'S DAMAGE, measured: {D['fights']} fights (Axiom "
                  f"both sides x 33 foes x seeds {seeds}), {len(dm)} landed "
                  f"echoes recorded at hurt; echoTally.landed = {D['landed']}")
            if len(dm) != D["landed"]:
                raise SystemExit("recorded echoes != echoTally.landed -- the "
                                 "wrap is not counting what it says it counts")
            qs = np.percentile(dm, [1, 10, 50, 90, 99])
            print(f"  mean {dm.mean():.2f}  p1 {qs[0]:.2f}  p10 {qs[1]:.2f}  "
                  f"p50 {qs[2]:.2f}  p90 {qs[3]:.2f}  p99 {qs[4]:.2f}  max "
                  f"{dm.max():.2f};  under 5.4 (the hit's weight floor) "
                  f"{np.mean(dm < 5.4):.1%}, under 1 {np.mean(dm < 1):.1%}")
            rec["dist"] = dict(n=len(dm), mean=float(dm.mean()),
                               p=dict(zip(["1", "10", "50", "90", "99"],
                                          map(float, qs))),
                               max=float(dm.max()),
                               below_floor=float(np.mean(dm < 5.4)),
                               below1=float(np.mean(dm < 1)))
            probe = [max(1.0, float(qs[0])), float(qs[1]), float(qs[2]),
                     float(qs[3]), float(qs[4])]
        else:
            probe = [3.0, 6.0, 11.6, 20.0, 30.0]
        print(f"\nSCALING -- the picked echo SCALED (rendered at its own dmg) "
              f"and FIXED (always at {a.dmg:g}), each against\n  the hit at "
              "that dmg; tf / td = the hit's own pitch and length there")
        print(f"  {'dmg':>6}{'tf Hz':>7}{'td ms':>7}{'hit pk':>8}{'hit st':>8}"
              f"{'SCALED pk':>11}{'st':>6}{'pk@':>6}{'FIXED pk':>10}{'st':>6}{'pk@':>6}")
        scal = []
        for dg in probe:
            hw = min(1.0, max(0.12, (dg or 10) / 45))
            _, H = M_([["play", T0, "hit", {"dmg": dg, "crit": False}]])
            _, Sc = M_([["cand", T0, "echo", ei, dg]])
            _, Fx = M_([["cand", T0, "echo", ei, a.dmg]])
            scal.append(dict(dmg=dg, tf=190 - 90 * hw, td=0.11 + 0.13 * hw,
                             hit_pk=H["peak"], hit_st=H["st"],
                             sc_pk=Sc["peak"] / H["peak"], sc_st=Sc["st"] / H["st"],
                             sc_at=Sc["pk_ms"], fx_pk=Fx["peak"] / H["peak"],
                             fx_st=Fx["st"] / H["st"], fx_at=Fx["pk_ms"]))
            s_ = scal[-1]
            print(f"  {dg:>6.2f}{s_['tf']:>7.0f}{s_['td'] * 1000:>7.0f}"
                  f"{H['peak']:>8.3f}{H['st']:>8.3f}{s_['sc_pk']:>11.2f}"
                  f"{s_['sc_st']:>6.2f}{s_['sc_at']:>6.0f}{s_['fx_pk']:>10.2f}"
                  f"{s_['fx_st']:>6.2f}{s_['fx_at']:>6.0f}")
        sc = [s_["sc_st"] for s_ in scal]
        fx = [s_["fx_st"] for s_ in scal]
        print(f"  st/hit across the dmg range: SCALED {min(sc):.2f}-{max(sc):.2f} "
              f"(x{max(sc) / min(sc):.2f}), FIXED {min(fx):.2f}-{max(fx):.2f} "
              f"(x{max(fx) / min(fx):.2f})")
        rec["scaling"] = scal

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("bands", "_draws")}
                for M in L]

    rec.update(cast=strip(cast), echo=strip(echo), hex=strip(hexr), wavs=sizes,
               pick={"cast": CAST_CANDIDATES[ci][0], "echo": ECHO_CANDIDATES[ei][0],
                     "hex": HEX_CANDIDATES[hi][0]})
    print(f"\nPICKS  cast {CAST_CANDIDATES[ci][0]}   echo {ECHO_CANDIDATES[ei][0]}"
          f"   hex {HEX_CANDIDATES[hi][0]}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, "
          "raw level -- not normalised, so they compare by ear)")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float))
    print("\n  NOTHING IS IN THE BUILD. The picks land as corollary_build.py "
          "stage-4 inserts, transcribed\n  with `this._` for the lab's "
          "helpers and every number checked against this file.")
    if FAILED:
        print(f"\nEXIT 1 -- no candidate passed for: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
