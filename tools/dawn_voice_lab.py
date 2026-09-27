#!/usr/bin/env python3
"""DAYBREAK'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v97.

    python dawn_voice_lab.py --game ../02-chain/sc-dawn.html --rows rows.json

v86 §4 SOUND, every word of it: "cast -- a slow swell rising over the whole
8s (re-struck tones stepping up a scale, one per second -- the only voice in
the roster tied to the window's clock); a tick -- nothing new (smite's);
close -- the top note held and released."  Rick, for the batch's art and
sound: "you pick i overrule". So this lab does not offer a spread -- it renders
five candidates a voice beside CONTROLS that can come back wrong, prints the
numbers each pick is made on, and PICKS by a rule written in this file
(`pick_*`). He overrules from one clip.

THE THREE EVENTS AND WHERE THEY FIRE (the voice is DRIVEN FROM `tickDawn`):
  cast   the bare id `ult/dawnbringer`, which `fireUlt` plays for every relic,
         is STEP 0 of the rise (a bare id must BE a voice -- v42's silent
         ultimate was a routing clause that reached nothing);
  steps  `ult/dawnbringer-step {n}` from `tickDawn`, n = 1..7, on the frame the
         window's own clock `D.t` crosses each whole second. That clock stops
         in a hit stop, so the rise stops with it; a caster who dies stops it;
  close  `ult/dawnbringer-close` from `tickDawn` on the frame the window runs
         out BY ITS CLOCK with the caster alive -- never on a death, never when
         the fight ends first.
  tick   SILENT. "nothing new (smite's)" -- and there is no smite voice
         anywhere in the build: `apply("smite")` plays nothing and `hurt`
         plays nothing (a ward broken by a tick plays the shatter's own `hit`,
         which is the engine's, not new). So a tick adds no sound.

THE WINDOW'S CLOCK IS NOT A WALL CLOCK -- measured here, and it shapes every
step candidate: a window-second is 1.00 s of match time only when nothing
lands in it. Over the survey the median is ~1.16 s and p99 ~1.62 s, because
every hit stop freezes `D.t` while the match clock (and the audio) runs on. A
step that holds for exactly one second leaves a GAP before most next steps.

THE CONTROLS, and what each one is for:
  old cast     the chord and bell Daybreak plays TODAY (the arm this replaces)
  hit @ 10.4   Dawnbringer's own blow, the sound "level sensible" is judged
               against (the line must sit under it: -6 dB at the top)
  BAR          Corollary's new chime (`ult/axiom`), v88's published pick --
               reproduced before anything new is quoted
  rune-crack   the shared fallback (`ult/spellbreaker`), reproduced likewise
  wall         the commonest sound inside a Dawn window (~57% of calls)
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9): step 0
               must be heard over it in its own third-octave
  RAW          the picked step's own code WITHOUT `.frequency.value = f` --
               the toolkit's plain `_tone`. It must come back WRONG: Chromium
               starts `_tone`'s oscillator phase off the param's 440 Hz default
               (its pitch event sits AT the start), so re-strikes above ~600 Hz
               land up to 180 degrees off and CANCEL instead of summing.

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext, the
    first event at t = 1.0, on a synth built the way `render.py` builds one
    (`Object.create` of the Sfx prototype, render.py's xorshift noise). The
    line itself is pure tone and draws no noise; the hit is judged on the
    worst of twelve noise draws. Nothing may sound before t = 1.0.
  * GAP SEQUENCES. Real Dawn windows are surveyed (Dawnbringer both sides x
    every foe x seeds): the match time of every step and of the close. A line
    is rendered on NOMINAL (every second 1.000 s) and on real windows at the
    p10 / p50 / p90 of window length and at the p99 single gap. Gates hold on
    EVERY sequence.
  * E50 = 50 ms RMS, 5 ms hop, in dB. PLATEAU of a step = median E50 over
    [onset + 0.35 s, min(next onset, onset + 1 s) - 0.05 s]. LEVEL of a step =
    the loudest 250 ms RMS inside its own second.
  * JUMP at a step change = max E50 in the 150 ms after the onset minus max E50
    in [-200, -20] ms before it: a struck note jumps from its own decayed tail.
    SAG = the previous plateau minus min E50 within 250 ms either side of the
    onset: the line dipping (or stopping) between degrees.
  * CLEAN = the new note's amplitude over the old note's, 150-350 ms after the
    onset (Hann-windowed projections at the two pitches): stepped, or smeared.
  * FLUTTER = p95 - p5 of the Hilbert envelope (dB) about its own 100 ms
    moving average, inside each plateau: re-strikes that read as a tremolo.
  * PITCH = the FFT peak (Hann, zero-padded, parabolic) inside the plateau, in
    cents from its degree of C major (C5 = 440 x 2^(3/12)).
  * IN-BAND = the RMS inside the third-octave around a pitch (FFT band sum).
    The score's is the p90 over 250 ms windows of an 8 s bed render.
  * DUCK = a hit @ 10.4 landing 0.6 s into the top step: the peak of (line +
    hit) - (line alone) in the hit's first 100 ms, over the hit alone. The
    line runs above the compressor's threshold for eight seconds; this is what
    that costs a blow.
  * CALL COST = the median main-thread time of one voice call (a step, or the
    close), timed in the page, 40 calls.
  * The candidates are LEVEL-MATCHED, not hand-set: each one's g0 and its
    per-step dB are solved (three passes) so that, after the chain, step 0 and
    step 7 land on the same two targets -- the centre of the window the level
    gates allow, with the swell at +9 dB -- so the pick is made on shape, not
    on which one happened to be loudest. The constants are rounded before any
    measured render, so the shipped arm is bit-for-bit what was measured.

THE PICKS, on Chromium 151.0.7922.34, sc-dawn fa8703a2e143f59d, seeds
97001-97003 (198 fights, 646 windows; a window-second p50 1.158 s, p99 1.617):

  step   4 HANDOFF  re-struck in phase every ~22 ms, held up to 1.75 s, the
                    next step stops what has not sounded. On every sequence:
                    jump <= 1.6 dB, sag <= 1.4, clean >= 14.0, swell +9.0,
                    flutter <= 1.2, 0 cents. Loudest 50 ms: step 0 -16.8 dB
                    under the hit @ 10.4 and +3.4 over the wall tick, step 7
                    -8.7 / +11.5; duck 0.93. 82 strikes, ~1.4 ms a call.
                    BELL out (eight hits: sag 46, jump 76); HELD passes the
                    nominal second and fails EVERY real one (a 1.61 s second:
                    sag 71 -- its note had stopped); ROLL out (flutter 7.6);
                    LEAN out (clean 6.7: a 0.9 s decay smears the degrees).
  close  1 STOP     held 522-535 ms, then -34 dB in 380 ms, gone 0.91 s after
                    the close, 0.1 dB dip at the join. FADE passes (held 600,
                    release 770) and loses the tiebreak; LONG, BRIEF, RING out.

  RAW (the control) comes back wrong: steps 6-7 ~10 dB down, swell -1.1..+0.4.
  FLUTTER was first taken on the Hilbert envelope, which reads one steady
  triangle strike as 2.2 dB (its own 3rd harmonic); it is now taken over
  whole periods, which read the same strike as 0.01-0.03 dB (printed).

THE TWO ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row is applied to `Sfx.prototype.play`'s own source in the page
    and rendered: it must reproduce the picked candidate to 1e-6, and `hit`
    through the patched play must be unchanged;
  * the tickDawn row is applied to `Match.prototype.tickDawn`'s own source and
    run on real fights beside the unpatched one: every fight identical
    (winner, clock, both hp, the dawn tally); per window closed by its clock,
    steps 1..7 once each and in order, then one close; no close after a death
    or a fight that ended first; the cast's bare id once per cast.
  Both anchors must occur exactly once in the game file.

AND THE TOOLKIT'S BUGS ARE DESIGNED AROUND, NOT FIXED: `_tone` only decays
(a held note is RE-STRUCK -- CLAUDE.md 4.5), and `_tone`'s phase (above). The
lab refuses any candidate source that names Math.random, rng or spawnFx, and
any _burst over 0.55 s or _sweep over 0.58 s.

Writes wavs to 05-reference/v97/ at RAW level (not normalised, so the files
compare by ear the way the numbers compare; gitignored with every wav).
Refuses to write silence. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
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
DEG = [0, 2, 4, 5, 7, 9, 11, 12]                       # C major, C5 -> C6
FREQ = [440 * 2 ** ((3 + d) / 12) for d in DEG]
SWELL_DB = 9.0                                         # step 7 over step 0

# ------------------------------------------------------------- THE STEPS ---
# One step a call. Every candidate draws the same eight pitches and is
# level-matched; they differ in how a degree is SOUNDED and HANDED ON.
#   every  re-strike spacing target, s (rounded to whole cycles); 0 = one strike
#   D      each strike's own decay, s (`_tone` dur)
#   len    how long a step keeps re-striking, s
#   hand   the next step stops this one's strikes that have not sounded yet
#   a0     the first strike carries a0 of the plateau (a soft re-strike)
#   fix    `.frequency.value = f` after `_tone` (see RAW)
STEP_CANDIDATES = [
    ("1 BELL", dict(every=0, D=1.2, len=0, hand=False, a0=0, fix=True,
                    type="triangle"),
     "one strike a second, ringing 1.2 s: the literal 'one per second'"),
    ("2 HELD", dict(every=0.022, D=0.5, len=1.0, hand=False, a0=0.6, fix=True,
                    type="triangle"),
     "re-struck in phase every ~22 ms for exactly its second"),
    ("3 ROLL", dict(every=0.100, D=0.6, len=1.75, hand=True, a0=0.6, fix=True,
                    type="triangle"),
     "a mallet roll, ~10 strikes/s, held until the next step takes over"),
    ("4 HANDOFF", dict(every=0.022, D=0.5, len=1.75, hand=True, a0=0.6,
                       fix=True, type="triangle"),
     "re-struck in phase every ~22 ms for up to 1.75 s; the next step stops "
     "what has not sounded"),
    ("5 LEAN", dict(every=0.040, D=0.9, len=1.75, hand=True, a0=0.6, fix=True,
                    type="triangle"),
     "HANDOFF at half the strikes: ~40 ms apart on a 0.9 s decay"),
]

STEP_SRC = r"""((S, sp) => (t, n, g0, kdb) => {
  const f = 440 * Math.pow(2, (3 + [0, 2, 4, 5, 7, 9, 11, 12][n]) / 12);
  const g = g0 * Math.pow(10, kdb * n / 20);
  const H = S.dawnHeld || (S.dawnHeld = []), P = n > 0 ? H[n - 1] : null;
  if (sp.hand && P){ for (const [o, at] of P.os) if (at >= t) try { o.stop(t); } catch(e){}
                     H[n - 1] = null; }
  const os = [];
  if (!sp.every){
    const o = S._tone(t, { freq: f, dur: sp.D, type: sp.type, gain: g });
    if (sp.fix) o.frequency.value = f;
    os.push([o, t]); H[n] = { t0: t, dt: 0, f, g, os }; return os.length;
  }
  const dt = Math.max(1, Math.round(f * sp.every)) / f;
  const q = Math.pow(0.0001 / g, dt / sp.D);
  for (let k = 0; k * dt < sp.len; k++){
    const o = S._tone(t + k * dt, { freq: f, dur: sp.D, type: sp.type,
                                    gain: k ? g : Math.max(g, g * sp.a0 / (1 - q)) });
    if (sp.fix) o.frequency.value = f;
    os.push([o, t + k * dt]);
  }
  H[n] = { t0: t, dt, f, g, os };
  return os.length;
})"""

# ------------------------------------------------------------- THE CLOSE ---
# "the top note held and released". Rendered AFTER the picked step's step 7,
# on the same synth: every candidate picks up step 7's strike grid IN PHASE
# (same start, same spacing), stopping the strikes of step 7 that have not
# sounded, so a hold carries on without a seam.
CLOSE_CANDIDATES = [
    ("1 STOP", dict(hold=0.5, fade=0, fdb=0, ring=False, D=0),
     "held 0.5 s, then the re-strikes stop: released on the note's own decay"),
    ("2 FADE", dict(hold=0.5, fade=0.5, fdb=30, ring=False, D=0),
     "held 0.5 s, then re-struck 30 dB softer over 0.5 s"),
    ("3 LONG", dict(hold=1.0, fade=1.0, fdb=30, ring=False, D=0),
     "held 1.0 s, faded over 1.0 s"),
    ("4 BRIEF", dict(hold=0.2, fade=0.5, fdb=30, ring=False, D=0),
     "held 0.2 s, faded over 0.5 s"),
    ("5 RING", dict(hold=0, fade=0, fdb=0, ring=True, D=1.5),
     "no hold: the top note struck once at the plateau and let ring 1.5 s "
     "(the control on 'held')"),
]

CLOSE_SRC = r"""((S, cp, sp, g0, kdb) => (t) => {
  const H = S.dawnHeld || (S.dawnHeld = []), P = H[7];
  const f = P ? P.f : 440 * Math.pow(2, 15 / 12);
  const g = P ? P.g : g0 * Math.pow(10, kdb * 7 / 20);
  const dt = P ? P.dt : Math.max(1, Math.round(f * sp.every)) / f, t0 = P ? P.t0 : t;
  let k = Math.ceil((t - t0) / dt - 1e-9);
  if (P){ for (const [o, at] of P.os) if (at >= t0 + (k - 0.5) * dt) try { o.stop(t); } catch(e){}
          H[7] = null; }
  if (cp.ring){
    const q = Math.pow(0.0001 / g, dt / sp.D);
    S._tone(t0 + k * dt, { freq: f, gain: g / (1 - q), dur: cp.D,
                           type: sp.type }).frequency.value = f;
    return 1;
  }
  let c = 0;
  for (; t0 + k * dt < t + cp.hold + cp.fade; k++){
    const s = t0 + k * dt, u = cp.fade ? Math.max(0, (s - t - cp.hold) / cp.fade) : 0;
    S._tone(s, { freq: f, gain: g * Math.pow(10, -cp.fdb * u / 20), dur: sp.D,
                 type: sp.type }).frequency.value = f;
    c++;
  }
  return c;
})"""

for _k, _src in (("step", STEP_SRC), ("close", CLOSE_SRC)):
    _bad = re.findall(r"Math\.random|\brng\b|spawnFx", _src)
    if _bad:
        raise SystemExit(f"REFUSING: the {_k} candidates name {_bad} -- a voice "
                         "must draw no random number.")

# ------------------------------------------------------------ THE ROWS -----
# The two edits to 02-chain/sc-dawn.html, generated from the pick and the
# rounded constants, then CHECKED in the page (see the docstring).
SFX_ANCHOR = '''        if (w === "dawnbringer"){                       // a chord and a bell
          [0, 7, 12, 16].forEach((st, i) =>
            this._tone(t + i * 0.03, { freq: 220 * Math.pow(2, st/12), gain: 0.13,
                                       dur: 1.5, type:"triangle" }));
          this._burst(t + 0.14, { freq: 5200, q: 0.9, gain: 0.20, dur: 0.5, type:"highpass" });'''

TICK_ANCHOR = '''      const D = f.ultDawn;
      if (!D) continue;
      D.t += dt;
      if (D.t >= D.dur || !f.alive){ f.ultDawn = null; continue; }'''

TICK_CODE = '''      const D = f.ultDawn;
      if (!D) continue;
      const sec = Math.floor(D.t);
      D.t += dt;
      /* DAYBREAK'S VOICE RIDES THIS CLOCK (v86 §4: "the only voice in the
         roster tied to the window's clock"). A step each time `D.t` crosses
         a whole second (`sec` is the second before this frame's add; the
         cast already played step 0), and the close when the window runs out
         with its caster alive: never on a death, and never once the fight
         is over, because step() stops calling this. Presentation only:
         SFX.play draws nothing, is a no-op headless, and nothing here is
         read back (dawn_voice_lab: fights identical with and without it). */
      if (f.alive && D.t >= D.dur) SFX.play("ult", { w: "dawnbringer-close" });
      else if (f.alive && Math.floor(D.t) > sec)
        SFX.play("ult", { w: "dawnbringer-step", n: Math.floor(D.t) });
      if (D.t >= D.dur || !f.alive){ f.ultDawn = null; continue; }'''


def fmt(v):
    """A constant as the arm prints it -- and as every measured render uses."""
    return repr(float(v)).rstrip("0").rstrip(".") if "e" not in repr(float(v)) else repr(float(v))


def arm_text(S_, C_, gaps, raw_drop):
    """The Sfx row's code, generated from the pick, the rounded constants and
    the numbers they were measured at; checked in the page before printing."""
    sp, g0, kdb, cp = S_["sp"], S_["g0"], S_["kdb"], C_["cp"]
    sname, cname = S_["name"], C_["name"]
    N_lo = max(1, round(FREQ[0] * sp["every"]))
    N_hi = max(1, round(FREQ[7] * sp["every"]))
    fade = cp["fade"]
    if fade:
        rel = (f"then re-strikes\n             it {fmt(cp['fdb'])} dB softer over {fmt(fade)} s and stops: "
               f"released, -34 dB {C_['rel_hi'] * 1000:.0f} ms\n             after the hold.")
        close_loop = (
            f'''          for (; t0 + k * dt < t + {fmt(cp['hold'])} + {fmt(fade)}; k++){{
            const s = t0 + k * dt, u = Math.max(0, (s - t - {fmt(cp['hold'])}) / {fmt(fade)});
            this._tone(s, {{ freq: f, gain: g * Math.pow(10, -{fmt(cp['fdb'])} * u / 20), dur: {fmt(sp['D'])},
                            type:"triangle" }}).frequency.value = f;
          }}''')
    else:
        rel = (f"then stops\n             re-striking and the note releases on its own "
               f"{fmt(sp['D'])} s decay, -34 dB\n             {C_['rel_hi'] * 1000:.0f} ms later.")
        close_loop = (
            f'''          for (; t0 + k * dt < t + {fmt(cp['hold'])}; k++)
            this._tone(t0 + k * dt, {{ freq: f, gain: g, dur: {fmt(sp['D'])},
                                      type:"triangle" }}).frequency.value = f;''')
    return f'''        if (w === "dawnbringer" || w === "dawnbringer-step"){{   // the sun rises
          /* DAYBREAK -- v86 §4 SOUND: "a slow swell rising over the whole 8s
             (re-struck tones stepping up a scale, one per second -- the only
             voice in the roster tied to the window's clock)". {sname.split()[1]}, of five,
             picked on the numbers by `dawn_voice_lab.py` under Rick's "you
             pick i overrule" (v97).

             ONE STEP A CALL. The bare id is the cast (`fireUlt` plays it for
             every relic) and is step 0; `tickDawn` plays steps 1-7 as the
             window's OWN clock crosses each second, and the close when it
             runs out -- so a hit stop, which freezes that clock, holds the
             note, and a caster who dies mid-window stops the rise. The eight
             steps are one octave of C major, C5 -> C6 (diatonic to the
             score's A minor), each {fmt(kdb)} dB over the last going in: +{fmt(SWELL_DB)} dB
             over the eight coming out of the chain, which compresses it.

             A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md 4.5), so a
             step is RE-STRUCK every {N_lo}-{N_hi} whole cycles (~{round(sp['every'] * 1000)} ms), in phase, for
             up to {fmt(sp['len'])} s -- a window-second runs {gaps['p50']:.2f} s of match time at the
             median and {gaps['p99']:.2f} s at p99, because every hit stop freezes the
             window's clock -- and the NEXT step stops each strike that has
             not sounded yet. The old note releases over its own {fmt(sp['D'])} s decay
             while the new one fills in: one line, handed from degree to
             degree however long the second runs. The first strike carries
             {fmt(sp['a0'])} of the plateau, so a degree re-strikes softly. `dawnHeld` keeps
             each step's strikes for the hand-off: presentation state on the
             synth, never read by the simulation.

             `.frequency.value = f` AFTER `_tone` IS LOAD-BEARING. `_tone`
             sets its pitch with an event AT the strike, and Chromium starts
             the oscillator's phase off the param's 440 Hz default: measured,
             a strike at 1046 Hz lands up to 180 degrees off, so re-strikes
             above ~600 Hz cancel instead of summing (the lab's RAW control:
             the top step {raw_drop:.0f} dB down and the swell gone). Setting the value
             puts every strike within one sample. */
          const n = w === "dawnbringer" ? 0 : Math.max(0, Math.min(7, p.n | 0));
          const f = 440 * Math.pow(2, (3 + [0, 2, 4, 5, 7, 9, 11, 12][n]) / 12);
          const g = {fmt(g0)} * Math.pow(10, {fmt(kdb)} * n / 20);
          const dt = Math.max(1, Math.round(f * {fmt(sp['every'])})) / f;
          const q = Math.pow(0.0001 / g, dt / {fmt(sp['D'])});
          const H = this.dawnHeld || (this.dawnHeld = []), P = n > 0 ? H[n - 1] : null;
          if (P){{ for (const [o, at] of P.os) if (at >= t) try {{ o.stop(t); }} catch(e){{}}
                  H[n - 1] = null; }}
          const os = [];
          for (let k = 0; k * dt < {fmt(sp['len'])}; k++){{
            const o = this._tone(t + k * dt, {{ freq: f, dur: {fmt(sp['D'])}, type:"triangle",
                                               gain: k ? g : Math.max(g, g * {fmt(sp['a0'])} / (1 - q)) }});
            o.frequency.value = f;
            os.push([o, t + k * dt]);
          }}
          H[n] = {{ t0: t, dt, f, g, os }};
        }} else if (w === "dawnbringer-close"){{          // held, and released
          /* "close -- the top note held and released" (v86 §4). {cname.split()[1]}, of five
             (`dawn_voice_lab.py`). It picks up step 7's strike grid IN PHASE
             -- the same start, the same spacing -- and stops step 7's strikes
             that have not sounded, so the hold carries on without a seam. It
             holds {fmt(cp['hold'])} s (the picture's wash fades over 0.5 s), {rel}
             `tickDawn` plays it only when the window closes by its clock,
             never on a death. */
          const H = this.dawnHeld || (this.dawnHeld = []), P = H[7];
          const f = P ? P.f : 440 * Math.pow(2, 15 / 12);
          const g = P ? P.g : {fmt(g0)} * Math.pow(10, {fmt(kdb)} * 7 / 20);
          const dt = P ? P.dt : Math.max(1, Math.round(f * {fmt(sp['every'])})) / f, t0 = P ? P.t0 : t;
          let k = Math.ceil((t - t0) / dt - 1e-9);
          if (P){{ for (const [o, at] of P.os) if (at >= t0 + (k - 0.5) * dt) try {{ o.stop(t); }} catch(e){{}}
                  H[7] = null; }}
{close_loop}'''


# ------------------------------------------------------------ THE RENDER ---
# events, each rendered at its own time on ONE synth (so the hand-off and the
# close's grid see the steps before them, exactly as a clip replays them):
#   ["play",  at, kind, p]          SFX.play(kind, p)
#   ["step",  at, i, n]             step candidate i (i = -1: RAW), degree n
#   ["close", at, j]                close candidate j after the picked step
#   ["arm",   at, kind, p]          the PATCHED play (the Sfx row applied)
RENDER_JS = r"""async ([evs, secs, seed, specs, cal, closes, pick, row]) => {
  const OC = window.OfflineAudioContext, sr = 48000;
  const proto = Object.getPrototypeOf(AC.SFX);
  const mkNoise = (oc) => {
    const n = Math.floor(sr * 0.6), nb = oc.createBuffer(1, n, sr);
    const d = nb.getChannelData(0); let s = (seed || 0x9e3779b9) >>> 0;
    for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17;
      s ^= s << 5; s >>>= 0; d[i] = (s / 4294967296) * 2 - 1; }
    return nb; };
  const oc = new OC(1, Math.round(sr * secs), sr);
  let cursor = 0;
  const S = Object.create(proto);
  S.ok = true; S.on = true;
  S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
    const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = mkNoise(oc);
  const log = { burst: [], sweep: [], tone: 0, calls: [] };
  S._burst = function(t, o, d){ log.burst.push(o.dur); return proto._burst.call(this, t, o, d); };
  S._sweep = function(t, o, d){ log.sweep.push(o.dur); return proto._sweep.call(this, t, o, d); };
  S._tone  = function(t, o, d){ log.tone++; return proto._tone.call(this, t, o, d); };
  const STEP = (0, eval)(window.__dawnStep), CLOSE = (0, eval)(window.__dawnClose);
  let patched = null;
  if (row){
    const src = proto.play.toString();
    const at = src.split(row[0]).length - 1;
    if (at !== 1) return { err: `the Sfx anchor occurs ${at} times in play()` };
    patched = (0, eval)("(function " + src.replace(row[0], () => row[1]) + ")");
  }
  for (const e of evs){
    cursor = e[1];
    const before = log.tone;
    if (e[0] === "play") S.play(e[2], e[3]);
    else if (e[0] === "step"){ const i = e[2]; STEP(S, specs[i < 0 ? specs.length - 1 : i])(e[1], e[3], cal[0], cal[1]); }
    else if (e[0] === "close") CLOSE(S, closes[e[2]], specs[pick], cal[0], cal[1])(e[1]);
    else if (e[0] === "arm") patched.call(S, e[2], e[3]);
    else if (e[0] === "steady")      /* one strike, in phase: the flutter metric's floor */
      S._tone(e[1], { freq: e[2], gain: e[3], dur: e[4], type: "triangle" }).frequency.value = e[2];
    log.calls.push(log.tone - before);
  }
  const buf = await oc.startRendering();
  const d = buf.getChannelData(0);
  const u8 = new Uint8Array(d.buffer, d.byteOffset, d.byteLength);
  let s = ""; for (let i = 0; i < u8.length; i += 0x8000)
    s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return { pcm: btoa(s), log };
}"""

BED_JS = r"""async ([secs]) => {
  /* the score exactly as cinema_clip mixes it: bed() on a plain bus, x0.9,
     summed after the SFX chain */
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

COST_JS = r"""([spec, g0, kdb, cp, reps]) => {
  const proto = Object.getPrototypeOf(AC.SFX);
  const oc = new OfflineAudioContext(1, 48000 * 8, 48000);
  const S = Object.create(proto); S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  const nb = oc.createBuffer(1, 28800, 48000); S.noise = nb;
  const STEP = (0, eval)(window.__dawnStep)(S, spec);
  const CLOSE = (0, eval)(window.__dawnClose)(S, cp, spec, g0, kdb);
  const one = [], cl = [];
  for (let i = 0; i < reps; i++){
    const a = performance.now(); STEP(0.5 + (i % 8) * 0.1, i % 8, g0, kdb); one.push(performance.now() - a);
    if (i % 8 === 7){ const b = performance.now(); CLOSE(0.5 + 0.8); cl.push(performance.now() - b); }
  }
  const a = performance.now();
  for (let i = 0; i < reps; i++) STEP(0.5 + (i % 8) * 0.1, i % 8, g0, kdb);
  const batch = (performance.now() - a) / reps;
  const med = (v) => v.slice().sort((x, y) => x - y)[v.length >> 1];
  return { step: med(one), batch, close: cl.length ? med(cl) : 0 };
}"""

# The survey: every Dawn window in real fights, its step times and how it
# ended, the sounds inside it, and the damage of every hit inside it.
SURVEY_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX;
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "dawnbringer");
  const wins = [], kinds = {}, hitd = []; let winSecs = 0, fights = 0, open = false;
  const orig = S.play;
  S.play = function(kind, p){
    if (open){ const k = kind + (p && p.w ? ":" + p.w : ""); kinds[k] = (kinds[k] || 0) + 1;
               if (kind === "hit") hitd.push(p.dmg); }
    return orig.call(this, kind, p); };
  try {
    for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
      const m = side ? new AC.Match(fid, "dawnbringer", sd) : new AC.Match("dawnbringer", fid, sd);
      const f = side ? m.b : m.a; let steps = 0, prev = null, W = null;
      while (!m.over && steps < 170 / DT){
        m.step(DT); steps++;
        const D = f.ultDawn;
        if (D && D !== prev){ W = { side, foe: fid, seed: sd, cast: m.t, steps: [], close: null, end: null };
                              wins.push(W); open = true; }
        if (D){ winSecs += DT; if (Math.floor(D.t) > W.steps.length) W.steps.push(m.t - W.cast); }
        if (!D && prev){ open = false;
          if (f.alive && prev.t + DT >= prev.dur - 1e-9){ W.end = "clock"; W.close = m.t - W.cast; }
          else W.end = "death"; }
        prev = D;
      }
      if (open){ W.end = "over"; open = false; }
      fights++;
    }
  } finally { S.play = orig; }
  return { wins, kinds, hitd, winSecs, fights };
}"""

# One real fight re-run, every SFX call recorded with its match time.
RECORD_JS = r"""([side, fid, sd]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, orig = S.play, ev = [];
  const m = side ? new AC.Match(fid, "dawnbringer", sd) : new AC.Match("dawnbringer", fid, sd);
  S.play = function(kind, p){ ev.push([m.t, kind, JSON.parse(JSON.stringify(p || {}))]);
                              return orig.call(this, kind, p); };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { S.play = orig; }
  return ev;
}"""

# The tickDawn row, applied to the real prototype and run beside the original.
WIRE_JS = r"""([seeds, anchor, code]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const orig = P.tickDawn, src = orig.toString();
  const at = src.split(anchor).length - 1;
  if (at !== 1) return { err: `the tickDawn anchor occurs ${at} times in tickDawn()` };
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src.replace(anchor, () => code) + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "dawnbringer");
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, "dawnbringer", sd) : new AC.Match("dawnbringer", fid, sd);
    const f = side ? m.b : m.a, calls = [], wins = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      if (kind === "ult" && p && typeof p.w === "string" && p.w.startsWith("dawnbringer"))
        calls.push([p.w, p.n === undefined ? null : p.n, m.t]);
      return op.call(this, kind, p); };
    if (wire) P.tickDawn = patched;
    let prev = null, W = null, n = 0;
    try {
      while (!m.over && n < 170 / DT){
        m.step(DT); n++;
        const D = f.ultDawn;
        if (D && D !== prev){ W = { cross: [], end: null, t: m.t }; wins.push(W); }
        if (D && Math.floor(D.t) > W.cross.length) W.cross.push(m.t);
        if (!D && prev) W.end = (f.alive && prev.t + DT >= prev.dur - 1e-9) ? "clock" : "death";
        prev = D;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickDawn = orig; if (had) S.play = op; else delete S.play; }
    const T = f.dawnTally || {};
    return { sum: [m.over, +m.t.toFixed(9), +m.a.hp.toFixed(9), +m.b.hp.toFixed(9),
                   T.casts || 0, T.ticks || 0, +(T.dealt || 0).toFixed(9)],
             calls, wins };
  };
  let fights = 0, same = 0, diff = [], windows = { clock: 0, death: 0, over: 0 }, bad = [];
  let steps = 0, closes = 0, casts = 0, lateMax = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (JSON.stringify(A.sum) === JSON.stringify(B.sum)) same++; else diff.push([side, fid, sd, A.sum, B.sum]);
    /* B's calls, split at each cast's bare id, against B's windows in order */
    const G = [];
    for (const c of B.calls){
      if (c[0] === "dawnbringer") G.push([c]);
      else if (G.length) G[G.length - 1].push(c);
      else bad.push([fid, sd, "a voice before any cast", c[0]]);
    }
    if (G.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", G.length, B.wins.length]);
    for (let wi = 0; wi < Math.min(G.length, B.wins.length); wi++){
      const W = B.wins[wi], mine = G[wi];
      windows[W.end]++;
      casts++;
      const st = mine.filter(c => c[0] === "dawnbringer-step"), cl = mine.filter(c => c[0] === "dawnbringer-close");
      steps += st.length; closes += cl.length;
      const ns = st.map(c => c[1]);
      if (JSON.stringify(ns) !== JSON.stringify(ns.slice().sort((a, b) => a - b))) bad.push([fid, sd, "steps out of order", ns]);
      if (W.end === "clock"){
        if (JSON.stringify(ns) !== "[1,2,3,4,5,6,7]") bad.push([fid, sd, "clock window steps", ns]);
        if (cl.length !== 1) bad.push([fid, sd, "clock window closes", cl.length]);
      } else if (cl.length) bad.push([fid, sd, W.end + " window played a close"]);
      st.forEach((c, i) => { const d = Math.abs(c[2] - W.cross[i]); lateMax = Math.max(lateMax, d);
                             if (!(d <= DT * 1.01)) bad.push([fid, sd, "step off its crossing", i + 1, d]); });
    }
  }
  return { fights, same, diff: diff.slice(0, 4), windows, steps, closes, casts, lateMax, bad: bad.slice(0, 12), nbad: bad.length };
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
    """RMS over `win` s every `hop` s: (linear, centre times)."""
    np = _np()
    W = int(SR * win); H = int(SR * hop)
    c = np.concatenate([[0.0], np.cumsum(x * x)])
    idx = np.arange(0, max(1, len(x) - W), H)
    r = np.sqrt(np.maximum(c[idx + W] - c[idx], 0) / W)
    return r, (idx + W / 2) / SR


def db(v):
    return 20 * math.log10(max(float(v), 1e-9))


def sel(ct, a, b):
    return (ct >= a) & (ct <= b)


def band_rms(x, fc, a, b):
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    X = np.fft.rfft(seg); fr = np.fft.rfftfreq(len(seg), 1 / SR)
    m = (fr >= fc / 2 ** (1 / 6)) & (fr < fc * 2 ** (1 / 6))
    return float(np.sqrt(2 * (np.abs(X[m]) ** 2).sum()) / len(seg))


def tone_amp(x, f, a, b):
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    w = np.hanning(len(seg)); n = np.arange(len(seg))
    return float(2 * abs((seg * w * np.exp(-2j * np.pi * f * n / SR)).sum()) / w.sum())


def cents(x, a, b, f):
    np = _np()
    seg = x[int(a * SR):int(b * SR)] * np.hanning(int(b * SR) - int(a * SR))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    m = np.nonzero((fr > f * 2 ** (-1 / 12)) & (fr < f * 2 ** (1 / 12)))[0]
    i = int(m[np.argmax(X[m])])
    y0, y1, y2 = np.log(X[i - 1:i + 2] + 1e-20)
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
    fm = (i + d) * SR / NF
    return 1200 * math.log2(fm / f), fm


def flutter_hilbert(x, a, b):
    """The FIRST flutter metric, kept only to print why it was replaced: the
    Hilbert envelope of a TRIANGLE is not flat -- its 3rd harmonic (1/9, sign
    alternating) swings |1 - e^{2ix}/9| between 8/9 and 10/9 every half
    cycle -- so it reads a perfectly steady triangle as ~2 dB of flutter."""
    np = _np()
    pad = int(0.06 * SR)
    i0, i1 = max(0, int(a * SR) - pad), int(b * SR) + pad
    seg = x[i0:i1]
    N = len(seg); Xf = np.fft.fft(seg); h = np.zeros(N); h[0] = 1
    h[1:(N + 1) // 2] = 2
    if N % 2 == 0:
        h[N // 2] = 1
    e = 20 * np.log10(np.maximum(np.abs(np.fft.ifft(Xf * h)), 1e-9))
    ma = np.convolve(e, np.ones(4800) / 4800, mode="same")
    k = slice(int(a * SR) - i0, int(b * SR) - i0)
    d = (e - ma)[k]
    return float(np.percentile(d, 95) - np.percentile(d, 5))


def flutter(x, a, b, f):
    """FLUTTER = p95 - p5, in dB, of the RMS over FOUR WHOLE PERIODS of the
    step's own pitch (1 ms hop) about its own 100 ms moving average, inside
    [a, b]. Whole periods, so the waveform's shape reads as nothing and only
    the level moving does (a single steady strike reads ~0: printed)."""
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


def line_metrics(x, on, end):
    """A rendered rise: `on` = the eight onsets (s, in the render), `end` =
    when the line is handed on after step 7 (the close)."""
    np = _np()
    r50, c50 = env(x, 0.05)
    e = 20 * np.log10(np.maximum(r50, 1e-5))      # floor -100 dBFS: silence reads as silence
    nxt = list(on[1:]) + [end]
    P, L, C, FL, FM = [], [], [], [], []
    for n in range(8):
        span = min(nxt[n] - on[n], 1.0)
        a, b = on[n] + 0.35, on[n] + span - 0.05
        P.append(float(np.median(e[sel(c50, a, b)])))
        r250, c250 = env(x[int(on[n] * SR):int((on[n] + span) * SR)], 0.25)
        L.append(db(r250.max()))
        c_, fm = cents(x, on[n] + 0.30, on[n] + span - 0.02, FREQ[n])
        C.append(c_); FM.append(fm)
        FL.append(flutter(x, a, b, FREQ[n]))
    J, SG, CL = [], [], []
    for n in range(1, 8):
        t = on[n]
        J.append(float(e[sel(c50, t, t + 0.15)].max() - e[sel(c50, t - 0.20, t - 0.02)].max()))
        SG.append(float(P[n - 1] - e[sel(c50, t - 0.25, t + 0.25)].min()))
        CL.append(db(tone_amp(x, FREQ[n], t + 0.15, t + 0.35) /
                     max(tone_amp(x, FREQ[n - 1], t + 0.15, t + 0.35), 1e-12)))
    return dict(P=P, L=L, cents=C, fm=FM, flut=FL, jump=J, sag=SG, clean=CL,
                swell=L[7] - L[0],
                mono=min(L[n] - L[n - 1] for n in range(1, 8)))


def close_metrics(x, on7, tc):
    np = _np()
    r50, c50 = env(x, 0.05)
    e = 20 * np.log10(np.maximum(r50, 1e-5))
    a = on7 + (0.35 if tc - on7 >= 0.5 else 0.25)
    P7 = float(np.median(e[sel(c50, a, tc - 0.03)]))
    dip = float(P7 - e[sel(c50, tc - 0.1, tc + 0.3)].min())
    i = int(np.searchsorted(c50, tc))
    k = i
    while k < len(e) and abs(e[k] - P7) <= 1.5:
        k += 1
    hold = float(c50[min(k, len(c50) - 1)] - tc)
    j = k
    while j < len(e) and e[j] > P7 - 34:
        j += 1
    rel = float(c50[min(j, len(c50) - 1)] - c50[min(k, len(c50) - 1)])
    seg = e[k:j + 1]
    rise = float((seg - np.minimum.accumulate(seg)).max()) if len(seg) else 0.0
    c_, fm = cents(x, tc + 0.05, tc + 0.35, FREQ[7])
    return dict(P7=P7, dip=dip, hold=hold, rel=rel, rise=rise, end=hold + rel,
                cents=c_, fm=fm)


def write_wav(path, x, start=T0 - 0.08):
    """Raw level -- NOT normalised -- from just before the first event to the
    end of the sound. Refuses silence (v42)."""
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
# pick wrong. Every gate is a word of v86 §4 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

STEP_RULE = (
    "on EVERY gap sequence: every degree within 25 cents of C major's and above "
    "the last ('stepping up a scale'); at every step change JUMP <= 6 dB and "
    "SAG <= 4 dB ('one rising line', not eight hits) and CLEAN >= 10 dB (a new "
    "degree, not a smear); step levels climb (each >= the last - 0.3 dB) by "
    "+6..+12 dB over the eight ('a slow swell rising over the whole 8s'); "
    "FLUTTER <= 3 dB (a swell, not a tremolo). Level: the top step's loudest "
    "50 ms <= 0.5x the hit's @ 10.4 on its quietest noise draw; step 0 IN-BAND "
    ">= 2x the score's p90 there (heard from the cast); DUCK >= 0.84 (a blow "
    "on the top step loses <= 1.5 dB). Tiebreak: the lowest worst SAG, then "
    "the fewest synth calls a step.")

CLOSE_RULE = (
    "on EVERY gap sequence: the top note (C6) within 25 cents; joined to step 7 "
    "with no dip > 3 dB; HELD within 1.5 dB of step 7's plateau for >= 400 ms "
    "after the close; RELEASED from the end of the hold to -34 dB in 0.3-1.0 s, "
    "never rising > 1 dB on the way; gone by 1.5 s. Tiebreak: the hold "
    "closest to 500 ms (the picture's wash fades over 0.5 s), then the release "
    "closest to 500 ms, then the fewest synth calls.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def step_why(M, lev):
    why = []
    if M["cents_w"] > 25: why.append(f"a degree {M['cents_w']:.0f} cents off")
    if not M["rising"]: why.append("a degree not above the last")
    if M["jump_w"] > 6: why.append(f"jump {M['jump_w']:.1f} dB > 6 ({M['jump_at']})")
    if M["sag_w"] > 4: why.append(f"sag {M['sag_w']:.1f} dB > 4 ({M['sag_at']})")
    if M["clean_w"] < 10: why.append(f"clean {M['clean_w']:.1f} dB < 10 ({M['clean_at']})")
    if M["mono_w"] < -0.3: why.append(f"a step {M['mono_w']:.1f} dB under the last")
    if not (6 <= M["swell_lo"] and M["swell_hi"] <= 12):
        why.append(f"swell {M['swell_lo']:.1f}..{M['swell_hi']:.1f} dB, not +6..+12")
    if M["flut_w"] > 3: why.append(f"flutter {M['flut_w']:.1f} dB > 3")
    if lev["top50"] > lev["hi"]: why.append(f"top 50 ms {lev['top50']:.4f} > {lev['hi']:.4f}")
    if lev["inb0"] < lev["lo"]: why.append(f"step 0 in-band {lev['inb0']:.4f} < {lev['lo']:.4f}")
    if lev["duck"] < 0.84: why.append(f"duck {lev['duck']:.2f} < 0.84")
    return why


def close_why(M):
    why = []
    if abs(M["cents_w"]) > 25: why.append(f"{M['cents_w']:.0f} cents off C6")
    if M["dip_w"] > 3: why.append(f"dip {M['dip_w']:.1f} dB at the join")
    if M["hold_w"] < 0.4: why.append(f"held {M['hold_w'] * 1000:.0f} ms < 400")
    if not (0.3 <= M["rel_lo"] and M["rel_hi"] <= 1.0):
        why.append(f"release {M['rel_lo'] * 1000:.0f}-{M['rel_hi'] * 1000:.0f} ms, not 300-1000")
    if M["rise_w"] > 1: why.append(f"rises {M['rise_w']:.1f} dB on the way down")
    if M["end_w"] > 1.5: why.append(f"sounding {M['end_w']:.2f} s after the close")
    return why


# render.py's seed first, then eleven other draws (the hit is noise-built)
NOISE_SEEDS = [0x9e3779b9] + [(0x2545F491 * (k + 7)) & 0xffffffff or 1
                              for k in range(11)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-dawn.html")
    ap.add_argument("--out", default="../05-reference/v97")
    ap.add_argument("--seeds", type=int, default=3, help="fight seeds a pairing")
    ap.add_argument("--seed0", type=int, default=97001)
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the two checked rows here")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"step": STEP_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx", SFX_ANCHOR), ("tickDawn", TICK_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    import hashlib
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nDAYBREAK -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  E50 = 50 ms RMS (5 ms hop), dB; PLATEAU = median E50 over [on+0.35, "
          "min(next, on+1) - 0.05] s; LEVEL = loudest 250 ms RMS in its second\n"
          "  JUMP = max E50 [0, 150] ms after an onset - max E50 [-200, -20] ms "
          "before; SAG = last plateau - min E50 within 250 ms of the onset\n"
          "  CLEAN = new/old note amplitude 150-350 ms in (Hann projections); "
          "FLUTTER = p95-p5 of the Hilbert envelope about its 100 ms mean\n"
          "  IN-BAND = RMS in the third-octave at a pitch; DUCK = a hit @ 10.4 "
          "0.6 s into the top step, (line+hit - line) peak / hit-alone peak\n"
          "  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, "
          "through Sfx.buildChain, render.py's xorshift noise")

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        page.evaluate("([a, b]) => { window.__dawnStep = a; window.__dawnClose = b; }",
                      [STEP_SRC, CLOSE_SRC])
        specs = [c[1] for c in STEP_CANDIDATES]
        closes = [c[1] for c in CLOSE_CANDIDATES]

        def R(evs, secs=3.0, seed=None, spec_list=None, cal=(0.0, 0.0), pick=0, row=None):
            r = page.evaluate(RENDER_JS, [evs, secs, seed, spec_list or specs, list(cal),
                                          closes, pick, row])
            assert not errors, errors[:3]
            x = pcm(r)
            for d_ in r["log"]["burst"]:
                if d_ > 0.55: raise SystemExit(f"REFUSING: a _burst of {d_}s in {evs[:2]}")
            for d_ in r["log"]["sweep"]:
                if d_ > 0.58: raise SystemExit(f"REFUSING: a _sweep of {d_}s in {evs[:2]}")
            if float(np.abs(x).max()) < 1e-6:
                raise SystemExit(f"SILENT render: {evs[:2]}")
            if float(np.abs(x[:int(T0 * SR) - 2]).max()) > 1e-6 and evs[0][1] >= T0:
                raise SystemExit(f"sound BEFORE t=1.0 in {evs[:2]}")
            return x, r["log"]

        sizes = {}

        def wav(name, x):
            sizes[name] = write_wav(out / name, x)

        # ---- THE WINDOW'S CLOCK, surveyed ----------------------------------
        seeds = [a.seed0 + k for k in range(a.seeds)]
        SV = page.evaluate(SURVEY_JS, [seeds])
        assert not errors, errors[:3]
        wins = SV["wins"]
        ends = {e: sum(1 for w in wins if w["end"] == e) for e in ("clock", "death", "over")}
        clockw = [w for w in wins if w["end"] == "clock" and len(w["steps"]) == 7]
        allg = np.array([g for w in wins for g in np.diff([0.0] + w["steps"] + ([w["close"]] if w["close"] else []))])
        gq = {k: float(np.percentile(allg, p)) for k, p in (("p10", 10), ("p50", 50), ("p90", 90), ("p99", 99))}
        gq["max"] = float(allg.max()); gq["late"] = float(np.mean(allg > 1.02))
        print(f"\nTHE WINDOW'S CLOCK -- {SV['fights']} fights (Dawnbringer both sides x "
              f"{len(set(w['foe'] for w in wins))} foes x seeds {seeds}), {len(wins)} windows: "
              f"{ends['clock']} closed by the clock, {ends['death']} by the caster's death, "
              f"{ends['over']} cut by the fight's end")
        print(f"  a window-second in match time (hit stops freeze D.t, not the clip): "
              f"n {len(allg)}  p10 {gq['p10']:.3f}  p50 {gq['p50']:.3f}  p90 {gq['p90']:.3f}"
              f"  p99 {gq['p99']:.3f}  max {gq['max']:.3f};  late by > 20 ms {gq['late']:.1%}")
        tot = sum(SV["kinds"].values())
        top = sorted(SV["kinds"].items(), key=lambda kv: -kv[1])[:6]
        print(f"  sounds inside the windows: {tot} calls, {tot / SV['winSecs']:.2f}/s -- " +
              ", ".join(f"{k} {v / tot:.1%}" for k, v in top))
        hd = np.array(SV["hitd"], dtype=float)
        print(f"  hit damage inside the windows: mean {hd.mean():.2f}, p50 {np.median(hd):.2f} "
              f"(Dawnbringer's blade: 10.4)")
        rec["clock"] = dict(fights=SV["fights"], windows=len(wins), ends=ends, gaps=gq,
                            sounds={k: v for k, v in top}, per_s=tot / SV["winSecs"])

        # the gap sequences every line is rendered on
        Lw = np.array([w["close"] for w in clockw])
        seqs = [("nominal", [float(k) for k in range(1, 8)], 8.0, None)]
        for tag, p_ in (("p10", 10), ("p50", 50), ("p90", 90)):
            w = clockw[int(np.argmin(np.abs(Lw - np.percentile(Lw, p_))))]
            seqs.append((f"{tag} {w['close']:.2f}s", w["steps"], w["close"], w))
        gp99 = gq["p99"]
        w99 = min(clockw, key=lambda w: abs(max(np.diff([0.0] + w["steps"] + [w["close"]])) - gp99))
        seqs.append((f"p99gap {max(np.diff([0.0] + w99['steps'] + [w99['close']])):.2f}s",
                     w99["steps"], w99["close"], w99))
        wmx = max(clockw, key=lambda w: max(np.diff([0.0] + w["steps"] + [w["close"]])))
        beyond = (f"maxgap {max(np.diff([0.0] + wmx['steps'] + [wmx['close']])):.2f}s",
                  wmx["steps"], wmx["close"], wmx)
        print("  gap sequences: " + "; ".join(
            f"{s[0]} [{', '.join(f'{g:.2f}' for g in np.diff([0.0] + list(s[1]) + [s[2]]))}]"
            for s in seqs))
        rec["seqs"] = [dict(tag=s[0], steps=list(s[1]), close=s[2],
                            src=None if s[3] is None else {k: s[3][k] for k in ("side", "foe", "seed", "cast")})
                       for s in seqs]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published BAR 0.364 / 300 ms / peak at 7 ms; rune-crack "
              "0.608 / 450 ms; hit@11.6 0.443 / 80 ms. They must come back.")

        def aud(x):
            y = x[int(T0 * SR):]
            e5, _ = env(y, 0.005, 0.005)
            on = np.nonzero(e5 > e5.max() * 0.02)[0]
            return (int(on[-1]) - int(on[0]) + 1) * 5.0

        ctl = {}
        for name, ev in (("old cast", ["play", T0, "ult", {"w": "dawnbringer"}]),
                         ("BAR", ["play", T0, "ult", {"w": "axiom"}]),
                         ("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                         ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                         ("hit@10.4", ["play", T0, "hit", {"dmg": 10.4, "crit": False}]),
                         ("wall", ["play", T0, "wall", {}])):
            x, _ = R([ev])
            y = x[int(T0 * SR):]
            r50, _c = env(y, 0.05)
            ctl[name] = dict(x=x, peak=float(np.abs(y).max()), pk_ms=float(np.argmax(np.abs(y)) / SR * 1000),
                             aud=aud(x), st50=float(r50.max()))
            print(f"  {name:<11} peak {ctl[name]['peak']:.3f} at {ctl[name]['pk_ms']:4.0f} ms   "
                  f"audible {ctl[name]['aud']:4.0f} ms   loudest 50 ms {ctl[name]['st50']:.4f}")
        repro = [("BAR peak", ctl["BAR"]["peak"], 0.364, 0.01), ("BAR audible", ctl["BAR"]["aud"], 300, 10),
                 ("rune-crack peak", ctl["rune-crack"]["peak"], 0.608, 0.01),
                 ("rune-crack audible", ctl["rune-crack"]["aud"], 450, 10),
                 ("hit@11.6 peak", ctl["hit@11.6"]["peak"], 0.443, 0.01),
                 ("hit@11.6 audible", ctl["hit@11.6"]["aud"], 80, 10)]
        bad = [f"{n}: {v:.3f} vs {p_}" for n, v, p_, t_ in repro if abs(v - p_) > t_]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
                                    f"PASS  all {len(repro)} published numbers come back"))
        if bad:
            raise SystemExit("the controls do not reproduce -- nothing new is quoted")
        wav("dawn-ctl-oldcast.wav", ctl["old cast"]["x"])
        wav("dawn-ctl-hit.wav", ctl["hit@10.4"]["x"])
        wav("dawn-ctl-bar.wav", ctl["BAR"]["x"])
        HD = []
        for sd in NOISE_SEEDS:
            x, _ = R([["play", T0, "hit", {"dmg": 10.4, "crit": False}]], seed=sd)
            HD.append(float(env(x[int(T0 * SR):], 0.05)[0].max()))
        hi = 0.5 * min(HD)
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [16.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        bedp90 = [float(np.percentile([band_rms(bseg, f, i / SR, i / SR + 0.25)
                                       for i in range(0, len(bseg) - 12000, 2400)], 90)) for f in FREQ]
        lo = 2 * bedp90[0]
        print(f"  the hit @ 10.4 across {len(NOISE_SEEDS)} draws: loudest 50 ms "
              f"{min(HD):.4f}-{max(HD):.4f}  -> the top step's ceiling {hi:.4f}")
        print("  the score's p90 in-band (clip mix): " +
              "  ".join(f"{['C5','D5','E5','F5','G5','A5','B5','C6'][i]} {v:.5f}" for i, v in enumerate(bedp90)) +
              f"  -> step 0's floor {lo:.4f}")
        room = db(hi) - db(lo) - SWELL_DB
        if room < 0:
            raise SystemExit(f"NO ROOM: the level window is {db(hi) - db(lo):.1f} dB and the swell "
                             f"is {SWELL_DB} -- nothing can pass")
        tgt0 = lo * 10 ** (room / 2 / 20)
        tgt7 = tgt0 * 10 ** (SWELL_DB / 20)
        print(f"  the window is {db(hi) - db(lo):.1f} dB for a {SWELL_DB:g} dB swell: targets "
              f"step 0 {tgt0:.4f}, step 7 {tgt7:.4f} ({db(tgt7 / min(HD)):.1f} dB re the hit), "
              f"{room / 2:.1f} dB from each gate")
        rec["levels"] = dict(hit_st50=HD, hi=hi, bedp90=bedp90, lo=lo, tgt0=tgt0, tgt7=tgt7)
        # the flutter metric's floor: ONE steady strike must read ~0
        fl_ = []
        for f_ in (FREQ[0], FREQ[7]):
            xs, _ = R([["steady", T0, f_, 0.02, 3.0]])
            fl_.append((flutter(xs, T0 + 0.35, T0 + 0.95, f_), flutter_hilbert(xs, T0 + 0.35, T0 + 0.95)))
        print("  FLUTTER's floor, one steady triangle strike: " +
              ", ".join(f"{n_} {a_:.2f} dB (the Hilbert envelope would read {b_:.2f})"
                        for n_, (a_, b_) in zip(("C5", "C6"), fl_)))
        if max(a_ for a_, _ in fl_) > 0.5:
            raise SystemExit("the flutter metric reads a steady tone as flutter -- nothing it says is usable")
        rec["flutter_floor"] = fl_

        # ---- LEVEL-MATCHING --------------------------------------------------
        def calibrate(i, spec_list):
            """g0 and the per-step dB that put step 0 and step 7, each rendered
            alone through the chain, on the two targets (the chain compresses,
            so this is solved, four passes). Rounded before use."""
            g0, kdb = 0.004, SWELL_DB / 7
            for _ in range(4):
                x0, _ = R([["step", T0, i, 0]], spec_list=spec_list, cal=(g0, kdb))
                x7, _ = R([["step", T0, i, 7]], spec_list=spec_list, cal=(g0, kdb))
                l0 = env(x0[int(T0 * SR):int((T0 + 1) * SR)], 0.25)[0].max()
                l7 = env(x7[int(T0 * SR):int((T0 + 1) * SR)], 0.25)[0].max()
                g7 = g0 * 10 ** (kdb * 7 / 20) * tgt7 / l7
                g0 = g0 * tgt0 / l0
                kdb = db(g7 / g0) / 7
            return float(f"{g0:.4g}"), round(kdb, 3)

        # ---- THE STEPS -----------------------------------------------------
        print(f"\nSTEPS -- 'a slow swell rising over the whole 8s (re-struck tones stepping "
              f"up a scale, one per second)'. C major C5 -> C6, +{SWELL_DB:g} dB after the chain.")
        print("  worst over the gap sequences; jump/sag/clean at every step change")
        H_ = (f"  {'cand':<11}{'g0':>8}{'dB/st':>7}{'calls':>6}{'cost ms':>8}{'jump':>6}{'sag':>6}"
              f"{'clean':>7}{'swell':>12}{'mono':>6}{'flut':>6}{'cents':>6}{'top50':>8}{'inb0':>8}{'duck':>6}")
        rows_s = []
        cand_list = list(STEP_CANDIDATES) + [("0 RAW", dict(STEP_CANDIDATES[3][1], fix=False),
                                              "HANDOFF without `.frequency.value = f`: the plain _tone")]
        specs_all = [c[1] for c in cand_list]
        seq_x = {}
        print(H_)
        for i, (name, sp, blurb) in enumerate(cand_list):
            if name == "0 RAW":
                g0, kdb = rows_s[3]["g0"], rows_s[3]["kdb"]       # HANDOFF's own gains
            else:
                g0, kdb = calibrate(i, specs_all)
            M = dict(name=name, g0=g0, kdb=kdb, sp=sp)
            per = []
            for (tag, st, cl, _w) in seqs:
                ons = [T0] + [T0 + s for s in st]
                ev = [["step", on, i, n] for n, on in enumerate(ons)]
                x, lg = R(ev, secs=T0 + cl + 2.5, spec_list=specs_all, cal=(g0, kdb))
                lm = line_metrics(x, ons, T0 + cl)
                lm["tag"] = tag; per.append(lm)
                seq_x[(i, tag)] = x
                if tag == "nominal":
                    M["calls"] = max(lg["calls"])
                    x2, _ = R(ev, secs=T0 + cl + 2.5, spec_list=specs_all, cal=(g0, kdb))
                    dd = float(np.abs(x - x2).max())
                    if dd > 1e-6:
                        raise SystemExit(f"{name} does not reproduce: two renders differ by {dd:.2e}")
                    wav(f"dawn-step-{name.replace(' ', '-').lower()}.wav", x)
                    r50, c50 = env(x, 0.05)
                    M["top50"] = float(r50[sel(c50, ons[7], T0 + cl)].max())
                    M["inb0"] = band_rms(x, FREQ[0], ons[0] + 0.35, ons[0] + 0.95)
            # the duck: a blow landing 0.6 s into the top step
            xl, _ = R([["step", T0, i, 7]], spec_list=specs_all, cal=(g0, kdb))
            xlh, _ = R([["step", T0, i, 7], ["play", T0 + 0.6, "hit", {"dmg": 10.4, "crit": False}]],
                       spec_list=specs_all, cal=(g0, kdb))
            xh, _ = R([["play", T0 + 0.6, "hit", {"dmg": 10.4, "crit": False}]])
            w_ = slice(int((T0 + 0.6) * SR), int((T0 + 0.7) * SR))
            M["duck"] = float(np.abs((xlh - xl)[w_]).max() / np.abs(xh[w_]).max())
            cost = page.evaluate(COST_JS, [sp, g0, kdb, CLOSE_CANDIDATES[0][1], 40])
            M["cost"] = cost["step"]; M["cost_batch"] = cost["batch"]
            def worst(key, f_=max):
                vals = [(v, p_["tag"], k + 1) for p_ in per for k, v in enumerate(p_[key])]
                v, tg, st_ = f_(vals, key=lambda z: z[0])
                return v, f"{tg}, step {st_}"
            M["jump_w"], M["jump_at"] = worst("jump")
            M["sag_w"], M["sag_at"] = worst("sag")
            M["clean_w"], M["clean_at"] = worst("clean", min)
            M["mono_w"] = min(p_["mono"] for p_ in per)
            M["swell_lo"] = min(p_["swell"] for p_ in per); M["swell_hi"] = max(p_["swell"] for p_ in per)
            M["flut_w"] = max(max(p_["flut"]) for p_ in per)
            M["cents_w"] = max(max(abs(c) for c in p_["cents"]) for p_ in per)
            M["rising"] = all(all(p_["fm"][k] > p_["fm"][k - 1] for k in range(1, 8)) for p_ in per)
            M["per"] = per
            lev = dict(top50=M["top50"], hi=hi, inb0=M["inb0"], lo=lo, duck=M["duck"])
            M["why"] = step_why(M, lev)
            rows_s.append(M)
            print(f"  {name:<11}{g0:>8.4g}{kdb:>7.3f}{M['calls']:>6d}{M['cost']:>8.2f}{M['jump_w']:>6.1f}"
                  f"{M['sag_w']:>6.1f}{M['clean_w']:>7.1f}{M['swell_lo']:>6.1f}-{M['swell_hi']:<5.1f}"
                  f"{M['mono_w']:>6.1f}{M['flut_w']:>6.1f}{M['cents_w']:>6.0f}{M['top50']:>8.4f}"
                  f"{M['inb0']:>8.4f}{M['duck']:>6.2f}   {blurb}")
        print(f"  gates: top50 <= {hi:.4f}, inb0 >= {lo:.4f}")
        for M in rows_s:
            p_ = M["per"][0]
            print(f"    {M['name']:<10} nominal: level/step " + " ".join(f"{v:5.1f}" for v in p_["L"]) +
                  "  | sag " + " ".join(f"{v:4.1f}" for v in p_["sag"]) +
                  "  | clean " + " ".join(f"{v:4.0f}" for v in p_["clean"]))
        print(f"  RULE  {STEP_RULE}")
        for M in rows_s:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        raw = rows_s.pop()          # the control is not a candidate
        if not raw["why"]:
            print("  THE RAW CONTROL PASSED -- it cannot fail, so it proves nothing")
            FAILED.append("raw control")
        else:
            print(f"  RAW (the control) comes back wrong, as it must: {'; '.join(raw['why'][:3])}")
        ok, fb = _gate(rows_s, "step")
        si = fb if ok is None else min(ok, key=lambda i: (round(rows_s[i]["sag_w"], 1), rows_s[i]["calls"]))
        S_ = rows_s[si]
        print(f"  PICK  {S_['name']}  g0 {S_['g0']}, {S_['kdb']} dB a step, {S_['calls']} strikes a call, "
              f"{S_['cost']:.2f} ms a call (batched {S_['cost_batch']:.2f})")
        p0 = S_["per"][0]
        x_ = seq_x[(si, "nominal")]
        r50, c50 = env(x_, 0.05)
        s0 = float(r50[sel(c50, T0, T0 + 1.0)].max())
        print(f"  its level, loudest 50 ms: step 0 {s0:.4f} / step 7 {S_['top50']:.4f} -- against the hit @ "
              f"10.4 {db(s0 / ctl['hit@10.4']['st50']):+.1f} / {db(S_['top50'] / ctl['hit@10.4']['st50']):+.1f} dB, "
              f"the wall tick {db(s0 / ctl['wall']['st50']):+.1f} / {db(S_['top50'] / ctl['wall']['st50']):+.1f} dB, "
              f"the old cast {db(s0 / ctl['old cast']['st50']):+.1f} / {db(S_['top50'] / ctl['old cast']['st50']):+.1f} dB")
        print(f"  its plateaus, nominal, dB: " + " ".join(f"{v:.1f}" for v in p0["P"]) +
              "  | flutter " + " ".join(f"{v:.1f}" for v in p0["flut"]) +
              "  | cents " + " ".join(f"{v:+.1f}" for v in p0["cents"]))
        tag, st, cl, _w = beyond
        ons = [T0] + [T0 + s for s in st]
        xb, _ = R([["step", on, si, n] for n, on in enumerate(ons)], secs=T0 + cl + 2.5, cal=(S_["g0"], S_["kdb"]))
        lb = line_metrics(xb, ons, T0 + cl)
        kx = int(np.argmax(lb["sag"]))
        print(f"  BEYOND p99 (reported, not gated): the survey's longest window-second, {tag} "
              f"[{', '.join(f'{g:.2f}' for g in np.diff([0.0] + list(st) + [cl]))}]: worst sag "
              f"{lb['sag'][kx]:.1f} dB at step {kx + 1} -- past {S_['sp']['len']} s the held note releases")
        rec["beyond"] = dict(tag=tag, sag=lb["sag"], jump=lb["jump"])

        # ---- THE CLOSE -----------------------------------------------------
        print("\nCLOSE -- 'the top note held and released', after the picked step's step 7, "
              "on every gap sequence")
        print(f"  {'cand':<9}{'calls':>6}{'cost ms':>8}{'dip':>6}{'held ms':>13}{'release ms':>13}"
              f"{'rise':>6}{'gone s':>7}{'cents':>7}")
        rows_c = []
        for j, (name, cp, blurb) in enumerate(CLOSE_CANDIDATES):
            per = []
            for (tag, st, cl, _w) in seqs:
                ons = [T0] + [T0 + s for s in st]
                ev = [["step", on, si, n] for n, on in enumerate(ons)] + [["close", T0 + cl, j]]
                x, lg = R(ev, secs=T0 + cl + 3.5, cal=(S_["g0"], S_["kdb"]), pick=si)
                cm = close_metrics(x, ons[7], T0 + cl); cm["tag"] = tag; per.append(cm)
                if tag == "nominal":
                    ncalls = lg["calls"][-1]
                    wav(f"dawn-close-{name.replace(' ', '-').lower()}.wav", x)
            cost = page.evaluate(COST_JS, [S_["sp"], S_["g0"], S_["kdb"], cp, 40])
            M = dict(name=name, cp=cp, calls=ncalls, cost=cost["close"], per=per,
                     dip_w=max(p["dip"] for p in per), hold_w=min(p["hold"] for p in per),
                     hold_hi=max(p["hold"] for p in per),
                     rel_lo=min(p["rel"] for p in per), rel_hi=max(p["rel"] for p in per),
                     rise_w=max(p["rise"] for p in per), end_w=max(p["end"] for p in per),
                     cents_w=max((p["cents"] for p in per), key=abs))
            M["why"] = close_why(M)
            rows_c.append(M)
            print(f"  {name:<9}{ncalls:>6d}{M['cost']:>8.2f}{M['dip_w']:>6.1f}{M['hold_w'] * 1000:>7.0f}-"
                  f"{M['hold_hi'] * 1000:<5.0f}{M['rel_lo'] * 1000:>7.0f}-{M['rel_hi'] * 1000:<5.0f}"
                  f"{M['rise_w']:>6.1f}{M['end_w']:>7.2f}{M['cents_w']:>7.1f}   {blurb}")
        print(f"  RULE  {CLOSE_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        ok, fb = _gate(rows_c, "close")
        ci = fb if ok is None else min(ok, key=lambda i: (round(abs(rows_c[i]["hold_w"] - 0.5), 2),
                                                          round(abs((rows_c[i]["rel_lo"] + rows_c[i]["rel_hi"]) / 2 - 0.5), 2),
                                                          rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}")

        # ---- THE ROWS, GENERATED AND CHECKED ---------------------------------
        raw_drop = S_["per"][0]["L"][7] - raw["per"][0]["L"][7]
        arm = arm_text(S_, C_, gq, raw_drop)
        bad_src = re.findall(r"Math\.random|\brng\b|spawnFx", arm + TICK_CODE)
        if bad_src:
            raise SystemExit(f"REFUSING: the rows name {bad_src}")
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        seqn = seqs[0]
        ons = [T0] + [T0 + s for s in seqn[1]]
        evA = ([["arm", T0, "ult", {"w": "dawnbringer"}]] +
               [["arm", on, "ult", {"w": "dawnbringer-step", "n": n}] for n, on in enumerate(ons) if n] +
               [["arm", T0 + seqn[2], "ult", {"w": "dawnbringer-close"}]])
        evC = ([["step", on, si, n] for n, on in enumerate(ons)] + [["close", T0 + seqn[2], ci]])
        xa, lga = R(evA, secs=T0 + seqn[2] + 3.5, cal=(S_["g0"], S_["kdb"]), pick=si, row=[SFX_ANCHOR, arm])
        xc, _ = R(evC, secs=T0 + seqn[2] + 3.5, cal=(S_["g0"], S_["kdb"]), pick=si)
        d_arm = float(np.abs(xa - xc).max())
        xh1, _ = R([["play", T0, "hit", {"dmg": 10.4, "crit": False}]])
        xh2, _ = R([["arm", T0, "hit", {"dmg": 10.4, "crit": False}]], row=[SFX_ANCHOR, arm])
        d_hit = float(np.abs(xh1 - xh2).max())
        x0a, _ = R([["arm", T0, "ult", {"w": "dawnbringer"}]], row=[SFX_ANCHOR, arm])
        pk0 = float(np.abs(x0a[int(T0 * SR):]).max())
        xca, _ = R([["arm", T0, "ult", {"w": "dawnbringer-close"}]], row=[SFX_ANCHOR, arm])
        pkc = float(np.abs(xca[int(T0 * SR):]).max())
        print(f"  the arm vs the picked candidates, nominal line + close: max |diff| {d_arm:.2e} "
              f"({'MATCH' if d_arm <= 1e-6 else 'MISMATCH'})")
        print(f"  `hit` through the patched play vs the original: max |diff| {d_hit:.2e}")
        print(f"  the BARE ID alone (the cast, step 0): peak {pk0:.3f};  the close alone "
              f"(no step 7 to pick up): peak {pkc:.3f} -- neither silent")
        if d_arm > 1e-6 or d_hit > 1e-6:
            FAILED.append("sfx row")
        wav("dawn-pick-nominal.wav", xa)
        rec["arm_check"] = dict(diff=d_arm, hit_diff=d_hit, bare_peak=pk0, close_alone_peak=pkc)

        print("\nTHE tickDawn ROW, applied to Match.prototype.tickDawn's own source, "
              "run beside the original on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds[:2], TICK_ANCHOR, TICK_CODE])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights: {WR['same']}/{WR['fights']} identical (over, clock, both hp, "
              f"casts, ticks, dealt)")
        print(f"  windows {WR['windows']}: {WR['casts']} cast voices, {WR['steps']} steps, {WR['closes']} "
              f"closes; every step on its own crossing (worst {WR['lateMax'] * 1000:.1f} ms);  "
              f"problems {WR['nbad']}")
        for b in WR["bad"]:
            print(f"    {b}")
        if WR["same"] != WR["fights"] or WR["nbad"] or WR["closes"] != WR["windows"]["clock"]:
            FAILED.append("tickDawn row")
        # the identity check's own control: the same row with ONE write the
        # simulation reads (the tick cooldown nudged 1 ms) must NOT come back
        # identical, or "identical" above proves nothing
        badc = TICK_CODE.replace("      D.t += dt;\n", "      D.t += dt;\n      D.cd -= 0.001;\n", 1)
        WB = page.evaluate(WIRE_JS, [seeds[:2], TICK_ANCHOR, badc])
        print(f"  the control (the row plus one sim write, D.cd -= 0.001): {WB['same']}/{WB['fights']} "
              f"identical -- {'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "windows", "casts", "steps", "closes", "lateMax", "nbad")}
        rec["wire"]["control_same"] = WB["same"]

        # ---- THE PICK IN A REAL WINDOW -------------------------------------
        w50 = seqs[2][3]
        EVs = page.evaluate(RECORD_JS, [w50["side"], w50["foe"], w50["seed"]])
        c0 = w50["cast"]
        fight = [["play", T0 + (t - c0), k, p] for (t, k, p) in EVs
                 if c0 - 1.0 <= t <= c0 + w50["close"] + 2.5 and
                 not (k == "ult" and str(p.get("w", "")).startswith("dawnbringer"))]
        fight = [e for e in fight if e[1] >= 0]
        ons = [T0] + [T0 + s for s in w50["steps"]]
        mine = ([["arm", T0, "ult", {"w": "dawnbringer"}]] +
                [["arm", on, "ult", {"w": "dawnbringer-step", "n": n}] for n, on in enumerate(ons) if n] +
                [["arm", T0 + w50["close"], "ult", {"w": "dawnbringer-close"}]])
        secs = T0 + w50["close"] + 3.0
        both = sorted(fight + mine, key=lambda e: e[1])
        xa_, _ = R(sorted(fight, key=lambda e: e[1]), secs=secs, row=[SFX_ANCHOR, arm])
        xb_, _ = R(both, secs=secs, row=[SFX_ANCHOR, arm])
        bd = bed[:len(xa_)]
        xa_ = xa_ + bd; xb_ = xb_ + bd
        over = []
        nxt = ons[1:] + [T0 + w50["close"]]
        for n in range(8):
            b_ = band_rms(xb_, FREQ[n], ons[n] + 0.2, nxt[n] - 0.05)
            a_ = band_rms(xa_, FREQ[n], ons[n] + 0.2, nxt[n] - 0.05)
            over.append(db(b_ / max(a_, 1e-12)))
        hits = [e[1] for e in fight if e[2] == "hit" and T0 <= e[1] <= T0 + w50["close"]]
        hr = [float(np.abs(xb_[int(h * SR):int((h + 0.03) * SR)]).max() /
                    max(np.abs(xa_[int(h * SR):int((h + 0.03) * SR)]).max(), 1e-9)) for h in hits]
        print(f"\nIN A REAL WINDOW -- {w50['foe']} (Dawnbringer side {w50['side']}), seed {w50['seed']}, "
              f"cast at {c0:.2f}s, closed by its clock at +{w50['close']:.2f}s; the fight's own "
              f"{len(fight)} sounds and the score, with and without the line")
        print("  the line over the fight in its own third-octave, per step: " +
              " ".join(f"{v:+.1f}" for v in over) + " dB")
        if hr:
            print(f"  the {len(hr)} blows inside the window keep {min(hr):.2f}-{max(hr):.2f} of their "
                  f"peak with the line under them (median {float(np.median(hr)):.2f})")
        wav("dawn-pick-real-window.wav", xb_)
        wav("dawn-pick-real-window-without.wav", xa_)
        rec["real"] = dict(foe=w50["foe"], seed=w50["seed"], side=w50["side"], over_db=over, blow_keep=hr)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("per",)} for M in L]

    rec.update(steps=strip(rows_s), raw={k: v for k, v in raw.items() if k != "per"},
               closes=strip(rows_c), wavs=sizes,
               pick={"step": S_["name"], "close": C_["name"], "g0": S_["g0"], "kdb": S_["kdb"]})
    print(f"\nPICKS  step {S_['name']}   close {C_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    rows = [dict(label="Sfx: Daybreak's voices (step + close) replace the chord and bell",
                 anchor=SFX_ANCHOR, mode="replace", code=arm),
            dict(label="tickDawn: the steps and the close ride the window's clock",
                 anchor=TICK_ANCHOR, mode="replace", code=TICK_CODE)]
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float))
    print("\n  NOTHING IS IN THE BUILD. The two rows are the edits; both were applied "
          "to the page's own code above.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
