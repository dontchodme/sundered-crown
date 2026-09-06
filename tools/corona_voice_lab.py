#!/usr/bin/env python3
"""FOUR CAST VOICES FOR CORONA, IN ONE FILE, FOR RICK TO PICK FROM. v66.

    python corona_voice_lab.py --game ../02-chain/sc-corona-fx.html

Brief stage 6, and rule 2: the ult sound is one of the seven things Rick gives
input on, and a spread is offered rather than a guess. v42 spread after four
serial failures; v43 spread first and the sound landed in one round trip.

WHAT THE CAST IS. A ring of light opens around the fighter and a star takes its
seat in the break. Nothing is struck, nothing lands, nothing is thrown -- for
up to 1.3 seconds after this sound the ultimate has touched nobody. So the
event is a THING SWITCHING ON AND STANDING, which is a register this roster has
almost none of: it is not an impact, not a throw and not a wind-up.

FOUR REGISTERS:

  1  KINDLE   a match into a bloom -- a bright transient, then a filtered
              swell that opens. The ring CATCHING.
  2  BELL     a struck inharmonic chord that rings out over a low body. The
              star, and the most "celestial" of the four.
  3  SWEEP    `_sweep` rising into a ring tone -- the band coming ROUND. Uses
              the primitive Scour's voice added to this toolkit.
  4  THRUM    a low fundamental switching on under a beating fifth. Something
              taking up STATION, and the only one that says "for a while".

## THE TOOLKIT'S TWO LIVE BUGS ARE DESIGNED AROUND, NOT HIT

CLAUDE.md 4.5, open item 6: `_burst` does NOT loop its 0.6s noise buffer, so
any burst longer than that plays silence for its tail; and `_tone` ends on an
exponential ramp over its whole length, so A HELD NOTE DOES NOT EXIST HERE --
anything that must last is RE-STRUCK. No burst below is over 0.55s and every
sustain is a re-strike on a clock.

## AND A SILENT ULTIMATE HAS SHIPPED THROUGH EVERY CHECK IN THIS REPO BEFORE

v42, section 4.1: a 14-check probe, a 29-check probe, a full sweep and a 13/13
verify all passed on an ultimate that made no sound, because `SFX.play` returns
on its first line headless and wraps its body in try/catch. So every candidate
here is RENDERED in an OfflineAudioContext and MEASURED -- peak, audible
duration and where its energy sits -- and the lab refuses to write a candidate
that renders silence.

Rendered through `buildChain`, the path that ships, at a NON-ZERO time: an
AudioParam whose first automation event is at t > 0 holds its constructor
default until then, so a bench that renders at zero measures a case the game
cannot produce. And v59's trap: `SFX_JS` schedules at `currentTime = 1.0`
inside a `secs`-long buffer, so a case list asking for 1.0 seconds renders
NOTHING.

Writes one wav and four singles. Touches no build.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

CANDIDATES = [
    ("1  KINDLE", "a match into a bloom -- the ring CATCHING light"),
    ("2  BELL",   "a struck inharmonic chord over a low body -- the STAR"),
    ("3  SWEEP",  "a rising sweep locking into a ring tone -- the band "
                  "coming ROUND"),
    ("4  THRUM",  "a low fundamental under a beating fifth -- taking up "
                  "STATION"),
]

VOICES_JS = r"""((S) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  const W = (t, o) => S._sweep(t, o);
  return [

  /* 1 -- KINDLE. A bright transient and then an OPENING: the swell is three
     re-struck low-passed bands at widening spacing, so the thing gets bigger
     rather than merely louder. The top tick at 0.02 is the catch itself; drop
     it and the swell has no beginning. */
  (t) => {
    B(t, { freq: 5200, q: 1.2, gain: 0.20, dur: 0.06, type:"highpass" });
    B(t + 0.02, { freq: 1900, q: 1.0, gain: 0.16, dur: 0.10, type:"bandpass" });
    T(t + 0.02, { freq: 320, to: 640, gain: 0.16, dur: 0.28, type:"triangle" });
    /* the bloom: three bands, each wider and later, none over 0.55s */
    [[0.06, 420, 0.9, 0.10, 0.34], [0.20, 700, 0.7, 0.09, 0.44],
     [0.40, 1050, 0.55, 0.07, 0.52]].forEach(([d, f, q, g, du]) =>
      B(t + d, { freq: f, q: q, gain: g, dur: du, type:"lowpass" }));
    /* and a rising pair under it, re-struck, because a held note does not
       exist in this toolkit */
    [0.00, 0.26, 0.52].forEach((d, i) =>
      T(t + d, { freq: 196 * Math.pow(1.26, i), to: 246 * Math.pow(1.26, i),
                 gain: 0.10 - i * 0.02, dur: 0.42, type:"sine" }));
    T(t + 0.30, { freq: 1568, to: 1568, gain: 0.045, dur: 0.60,
                  type:"triangle" });
  },

  /* 2 -- BELL. Inharmonic partials so it is a STRUCK OBJECT and not a musical
     note -- `sentinel_hum_lab`'s GLASS RING is the reference, and it is the
     candidate that still reads at low volume. Re-struck once, quietly, at
     0.42 so the ring is heard settling rather than simply decaying. */
  (t) => {
    const hit = (t0, g) => {
      [[262,1.00,1.30],[392,0.62,1.10],[551,0.40,0.90],[823,0.22,0.70],
       [1187,0.12,0.55]].forEach(([f, k, d]) =>
        T(t0, { freq: f, to: f * 0.9915, gain: 0.085 * k * g, dur: d,
                type:"triangle" }));
      B(t0, { freq: 4200, q: 1.8, gain: 0.055 * g, dur: 0.04,
              type:"bandpass" });
    };
    hit(t, 1.0);
    hit(t + 0.42, 0.34);
    /* the body, so the strike has a floor under it and does not read thin */
    T(t, { freq: 98, to: 88, gain: 0.13, dur: 0.75, type:"sine" });
    T(t + 0.42, { freq: 131, to: 124, gain: 0.05, dur: 0.55, type:"sine" });
  },

  /* 3 -- SWEEP. The band coming round, using `_sweep` -- the primitive Scour's
     voice added to this toolkit, and the only one in it that is a SWEPT noise
     rather than a struck one. It arrives and then LOCKS: the ring tone under
     the tail is what says the thing has taken its shape. */
  (t) => {
    W(t, { f0: 240, f1: 2600, q: 0.8, gain: 0.16, dur: 0.52, atk: 0.16 });
    W(t + 0.34, { f0: 1800, f1: 700, q: 1.1, gain: 0.085, dur: 0.40,
                  atk: 0.10 });
    B(t + 0.50, { freq: 900, q: 1.4, gain: 0.10, dur: 0.12, type:"bandpass" });
    /* the lock -- two re-struck triangles a fifth apart, the ring standing */
    [0.50, 0.86].forEach((d, i) => {
      T(t + d, { freq: 294, to: 294, gain: 0.10 - i * 0.03, dur: 0.50,
                 type:"triangle" });
      T(t + d, { freq: 441, to: 441, gain: 0.055 - i * 0.02, dur: 0.44,
                 type:"triangle" });
    });
    T(t + 0.02, { freq: 140, to: 190, gain: 0.11, dur: 0.46, type:"sine" });
  },

  /* 4 -- THRUM. Something taking up station: a low fundamental switching on
     under a fifth DETUNED just enough to beat against it, which is what says
     "this is going to be here a while" without a held note existing. The beat
     period is ~1.7 Hz by construction (294 against 292.3). */
  (t) => {
    B(t, { freq: 380, q: 0.7, gain: 0.11, dur: 0.20, type:"lowpass" });
    [0.00, 0.30, 0.60, 0.90].forEach((d, i) => {
      const g = 0.10 * (1 - i * 0.16);
      T(t + d, { freq: 73, to: 71, gain: g * 1.1, dur: 0.46, type:"sine" });
      T(t + d, { freq: 146, to: 146, gain: g * 0.55, dur: 0.42,
                 type:"sawtooth" });
      T(t + d, { freq: 292.3, to: 292.3, gain: g * 0.30, dur: 0.40,
                 type:"triangle" });
      T(t + d, { freq: 294.0, to: 294.0, gain: g * 0.30, dur: 0.40,
                 type:"triangle" });
    });
    B(t + 0.04, { freq: 2600, q: 1.1, gain: 0.05, dur: 0.08, type:"bandpass" });
  },

  ];
})"""


# ---------------------------------------------------------- THE STAR POP ----
# The second voice of the three the brief still owes. THE POP IS THE
# SET-PIECE: a star the size of the ball bursts into sixteen that scatter and
# bounce, and it is the moment the ultimate stops being a ring and becomes a
# room full of hazards.
#
# IT LANDS ~1.3s AFTER THE CAST, WHICH IS THE HARD CONSTRAINT. SWEEP runs
# 1.15s with its lock at 294/441 Hz and a centroid of 350 Hz, so a pop in that
# same band arrives while the cast is still ringing and the two fuse into one
# long noise. Every candidate below is deliberately somewhere else -- brighter,
# harder, or carrying a low transient the cast does not have.
POP_CANDIDATES = [
    ("1  SHATTER", "glass going -- a bright break and high pieces scattering"),
    ("2  FLARE",   "a magnesium pop -- a low thump under a bright bloom"),
    ("3  CHIMES",  "a struck cluster spraying small bells -- the STAR broke"),
    ("4  SCATTER", "a dry crack and then SIXTEEN ticks leaving, countable"),
]

POP_VOICES_JS = r"""((S) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  const W = (t, o) => S._sweep(t, o);
  /* ONE DETERMINISTIC HASH, standing in for the randomness these must not
     have: index in, a number in [0,1) out, stable for the life of the build.
     `drawScour` uses the same one. */
  const h = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
                     return x - Math.floor(x); };
  return [

  /* 1 -- SHATTER. Glass: a bright break, then the PIECES. The pieces are what
     separates this from an explosion -- ten short bandpassed ticks spreading
     over 0.3s, because at arena scale what has to read is "it came apart" and
     not "it went off". */
  (t) => {
    B(t, { freq: 3800, q: 0.7, gain: 0.30, dur: 0.09, type:"highpass" });
    B(t, { freq: 1400, q: 1.1, gain: 0.18, dur: 0.14, type:"bandpass" });
    T(t, { freq: 420, to: 90, gain: 0.20, dur: 0.24, type:"triangle" });
    for (let i = 0; i < 10; i++){
      const j = h(i * 3 + 1);
      B(t + 0.05 + i * 0.026 + j * 0.02,
        { freq: 2400 + j * 3000, q: 3.4, gain: 0.075 * (1 - i / 12),
          dur: 0.030, type:"bandpass" });
    }
  },

  /* 2 -- FLARE. The one that says DETONATION: a low thump the cast has no
     equivalent of, and a bright bloom over it. `_sweep` rising is what makes
     it open outward rather than simply hit -- sixteen things leaving, not one
     thing landing. */
  (t) => {
    T(t, { freq: 150, to: 40, gain: 0.34, dur: 0.45, type:"sine" });
    B(t, { freq: 220, q: 0.5, gain: 0.26, dur: 0.40, type:"lowpass" });
    W(t + 0.02, { f0: 900, f1: 5200, q: 0.7, gain: 0.15, dur: 0.42,
                  atk: 0.05 });
    B(t + 0.12, { freq: 4200, q: 0.5, gain: 0.09, dur: 0.50,
                  type:"highpass" });
    T(t + 0.04, { freq: 660, to: 240, gain: 0.10, dur: 0.30,
                  type:"triangle" });
  },

  /* 3 -- CHIMES. The celestial one, and the only candidate that says STAR
     rather than BOMB. A struck inharmonic cluster and then a spray of small
     partials scattering off it -- the same grammar as the cast's rejected
     BELL, moved up an octave and given somewhere to go. */
  (t) => {
    [[523,1.00],[784,0.60],[1109,0.38],[1567,0.22]].forEach(([f, k]) =>
      T(t, { freq: f, to: f * 0.992, gain: 0.10 * k, dur: 0.85,
             type:"triangle" }));
    B(t, { freq: 5200, q: 1.4, gain: 0.16, dur: 0.05, type:"bandpass" });
    T(t, { freq: 131, to: 118, gain: 0.16, dur: 0.40, type:"sine" });
    for (let i = 0; i < 8; i++){
      const j = h(i * 7 + 5);
      T(t + 0.06 + i * 0.042, { freq: 1200 + j * 2400,
                                to: (1200 + j * 2400) * 0.985,
                                gain: 0.055 * (1 - i / 10), dur: 0.34,
                                type:"triangle" });
    }
  },

  /* 4 -- SCATTER. A dry crack and then SIXTEEN ticks leaving, one per star,
     spread over 0.38s and just about countable. It is the only candidate that
     carries the ultimate's own number -- and the number is the mechanic: Rick
     took 16 over 10 and 6, and the shower is ~60% of the fire. */
  (t) => {
    B(t, { freq: 1800, q: 1.2, gain: 0.32, dur: 0.05, type:"bandpass" });
    T(t, { freq: 260, to: 60, gain: 0.22, dur: 0.16, type:"square" });
    B(t, { freq: 300, q: 0.6, gain: 0.16, dur: 0.22, type:"lowpass" });
    for (let i = 0; i < 16; i++){
      const j = h(i * 11 + 3);
      /* SPREAD, NOT EVEN. An even sixteen at this rate is a buzz; the wander
         is what makes them separate objects -- ARC CRACKLE's finding. */
      const d = 0.045 + i * 0.021 + (j - 0.5) * 0.014;
      B(t + d, { freq: 1500 + j * 1800, q: 4.0,
                 gain: 0.055 * (1 - i / 22), dur: 0.022, type:"bandpass" });
      if (i % 4 === 0)
        T(t + d, { freq: 880 + j * 400, to: 500, gain: 0.030, dur: 0.10,
                   type:"triangle" });
    }
  },

  ];
})"""


# ------------------------------------------- THE BURN AND THE CHAIN ---------
# The last two of the three voices the brief owes, and Rick delegated the pick:
# "pick voices for the burn and the chain."
#
# THE RATE IS THE WHOLE DESIGN CONSTRAINT AND IT IS DIFFERENT FOR EACH.
#
#   THE BURN ticks 120 times a second and is applied ~34 times a cast, so
#   NEITHER of those can carry a sound. It rides the CROSSING instead -- the
#   same gate the status tag uses, ~5.6 a cast -- which is a cue rate the
#   roster already lives with. Anything longer than ~0.2s or louder than a
#   background texture becomes the fight's dominant sound within one window.
#
#   THE CHAIN fires ~3.4 times a cast at 70ms apart, which is FASTER than any
#   voice can decay. So the candidates are built to be heard as ONE gesture
#   made of parts rather than as three separate sounds -- and the part that
#   varies is pitch, stepped by the star's index, because Rick's own sentence
#   is "a chain reaction like effect from one end of the arena to the other"
#   and the queue really is ordered top to bottom.
BURN_CANDIDATES = [
    ("1  SIZZLE", "a short wet hiss -- the crossing CATCHES"),
    ("2  WHUMP",  "a low soft ignition, almost under the fight"),
    ("3  TICK",   "a dry high tick with a hiss tail -- the driest of the three"),
]

CHAIN_CANDIDATES = [
    ("1  FALLING", "pitch steps DOWN with each star -- top of the hall first"),
    ("2  RISING",  "pitch steps UP -- the same gesture, run the other way"),
    ("3  FLAT",    "no step at all, a control: three of the same sound"),
]

BURN_VOICES_JS = r"""((S) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  return [
  /* 1 -- SIZZLE. Mid-band noise with a short low body under it. Sits between
     SWEEP (350 Hz centroid) and CHIMES (800) rather than on either. */
  (t) => {
    B(t, { freq: 2600, q: 1.0, gain: 0.085, dur: 0.16, type:"bandpass" });
    B(t + 0.02, { freq: 900, q: 0.7, gain: 0.050, dur: 0.14, type:"lowpass" });
    T(t, { freq: 240, to: 150, gain: 0.055, dur: 0.13, type:"triangle" });
  },
  /* 2 -- WHUMP. Gas catching: almost all of it under 400 Hz, which is where
     neither of the settled voices lives -- so it separates by REGISTER and can
     be quiet enough to fire six times a cast without stacking up. */
  (t) => {
    B(t, { freq: 300, q: 0.5, gain: 0.11, dur: 0.20, type:"lowpass" });
    T(t, { freq: 110, to: 62, gain: 0.085, dur: 0.22, type:"sine" });
    B(t + 0.03, { freq: 1800, q: 1.2, gain: 0.028, dur: 0.07,
                  type:"bandpass" });
  },
  /* 3 -- TICK. The driest: a single high tick and a thin tail. It is the one
     that will never mask anything and the one most likely to be missed. */
  (t) => {
    B(t, { freq: 4600, q: 1.6, gain: 0.075, dur: 0.045, type:"bandpass" });
    B(t + 0.03, { freq: 3200, q: 0.8, gain: 0.030, dur: 0.13,
                  type:"highpass" });
    T(t, { freq: 520, to: 320, gain: 0.030, dur: 0.09, type:"triangle" });
  },
  ];
})"""

CHAIN_VOICES_JS = r"""((S, i, n) => {
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);
  /* `i` IS THE STAR'S PLACE IN THE QUEUE and `n` how many there are, so the
     gesture knows where it is in itself. Nothing else in this game's audio
     takes an index; the chain needs one because 70ms apart is faster than any
     voice here decays, and three identical strikes at that spacing are a
     stutter rather than a run. */
  const k = n > 1 ? i / (n - 1) : 0;
  return [
  /* 1 -- FALLING. Down a fifth across the run. The queue is sorted by `y` and
     fires from the TOP of the hall, so a falling pitch runs the same way the
     eye does. */
  (t) => {
    const f = 880 * Math.pow(0.5, k * 0.58);
    B(t, { freq: 2200, q: 1.5, gain: 0.11, dur: 0.05, type:"bandpass" });
    T(t, { freq: f, to: f * 0.72, gain: 0.085, dur: 0.20, type:"triangle" });
    T(t, { freq: f * 0.5, to: f * 0.42, gain: 0.045, dur: 0.24,
           type:"sine" });
  },
  /* 2 -- RISING. The same gesture run the other way -- included because "which
     way a sequence should move" is exactly the kind of thing that is obvious
     only once both are heard. */
  (t) => {
    const f = 620 * Math.pow(2, k * 0.58);
    B(t, { freq: 2200, q: 1.5, gain: 0.11, dur: 0.05, type:"bandpass" });
    T(t, { freq: f, to: f * 1.18, gain: 0.085, dur: 0.20, type:"triangle" });
    T(t, { freq: f * 0.5, to: f * 0.56, gain: 0.045, dur: 0.24,
           type:"sine" });
  },
  /* 3 -- FLAT. THE CONTROL, and it is meant to be worse: the identical sound
     three times at 70ms. If this is indistinguishable from the other two then
     the step is doing nothing and the chain does not need an index. */
  (t) => {
    B(t, { freq: 2200, q: 1.5, gain: 0.11, dur: 0.05, type:"bandpass" });
    T(t, { freq: 740, to: 560, gain: 0.085, dur: 0.20, type:"triangle" });
    T(t, { freq: 370, to: 300, gain: 0.045, dur: 0.24, type:"sine" });
  },
  ];
})"""


RENDER_JS = r"""async ([gap, secs, only, voices]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  /* THE FOUR ARE A SHARED CONSTANT, not a copy. `corona_voice_audition.py`
     renders these same functions INTO A REAL FIGHT, and a hand-copied recipe
     in a second file is how the lab and the audition come to disagree about
     what was auditioned. */
  const V = eval(voices)(S);

  const idx = only >= 0 ? [only] : V.map((_, i) => i);
  idx.forEach((i, k) => V[i](1.0 + k * gap));

  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){ out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v; }
  return { pcm: out, sr, peak: +peak.toFixed(4), n: idx.length };
}"""


def write_wav(path, pcm, sr, norm=0.92):
    import numpy as np
    d = np.asarray(pcm, dtype=np.float32)
    top = float(np.abs(d).max())
    if top < 1e-6:
        raise SystemExit(
            f"REFUSING TO WRITE {path.name} -- it rendered SILENCE.\n"
            "  That is v42's defect exactly: `SFX.play` returns on its first\n"
            "  line headless and wraps its body in try/catch, so a silent\n"
            "  ultimate passes every other check in this repo.")
    pcm = np.clip(d * norm / top, -1, 1)
    w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()
    return top


def measure(pcm, sr):
    """Peak, audible length and where the energy sits.

    A number a person can be wrong about, rather than "it sounds fine": the
    audible span is the run from the first to the last sample over 1% of peak,
    and the low share is the fraction of energy under 120 Hz, which is what
    Deadfall's explosion was re-cut against (0.224 -> 0.553).
    """
    import numpy as np
    d = np.asarray(pcm, dtype=np.float32)
    top = float(np.abs(d).max())
    if top < 1e-6:
        return dict(peak=0.0, dur=0.0, low=0.0)
    idx = np.nonzero(np.abs(d) > top * 0.01)[0]
    dur = (idx[-1] - idx[0]) / sr if len(idx) else 0.0
    F = np.fft.rfft(d * np.hanning(len(d)))
    mag = np.abs(F) ** 2
    fr = np.fft.rfftfreq(len(d), 1 / sr)
    tot = mag.sum() or 1.0
    return dict(peak=top, dur=float(dur),
                low=float(mag[fr < 120].sum() / tot),
                cen=float((mag * fr).sum() / tot))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--gap", type=float, default=2.6)
    ap.add_argument("--out", default="../05-reference/v66/corona-cast-voices.wav")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    secs = 1.0 + a.gap * len(CANDIDATES) + 1.5

    print(f"\nCORONA -- {len(CANDIDATES)} CAST VOICES, one every {a.gap:g}s\n")
    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RENDER_JS, [a.gap, secs, -1, VOICES_JS])
        assert not errors, errors[:3]
        write_wav(out, r["pcm"], r["sr"])
        print(f"  {out.name}   raw peak {r['peak']}\n")
        # AND EACH ONE ON ITS OWN, because a spread played end to end is heard
        # as a comparison and a single is heard as the thing.
        print(f"  {'candidate':<12}{'peak':>8}{'audible':>9}{'<120Hz':>8}"
              f"{'centroid':>10}")
        for i, (name, blurb) in enumerate(CANDIDATES):
            one = page.evaluate(RENDER_JS, [a.gap, 3.2, i, VOICES_JS])
            assert not errors, errors[:3]
            p = out.with_name(out.stem + f"-{i + 1}.wav")
            write_wav(p, one["pcm"], one["sr"])
            M = measure(one["pcm"], one["sr"])
            print(f"  {name:<12}{M['peak']:>8.3f}{M['dur']:>8.2f}s"
                  f"{M['low']:>8.1%}{M['cen']:>9.0f}Hz   {blurb}")
    print("\n  NOTHING IS IN THE BUILD. The cast currently plays the generic\n"
          "  `rune-crack` fallback, which is what an unnamed `w` gets in\n"
          "  `SFX.play`. The pick lands as a builder insert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
