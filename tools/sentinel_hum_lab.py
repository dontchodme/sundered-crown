#!/usr/bin/env python3
"""FOUR CANDIDATE BEAM SUSTAINS, IN ONE FILE, FOR RICK TO PICK FROM.

    python sentinel_hum_lab.py --out ../05-reference/v48-sentinel/hum-candidates.wav

WHY THIS EXISTS, AND WHY IT IS A RUN AND NOT A HIT. Sentinel already has four
voices -- the wind-up, the release, a pass and the tip -- and the beam is still
SILENT for most of its own duration, because all four are events and the beam
is a state. It stands for four to nine seconds with nothing under it.

**THE TOOLKIT CANNOT HOLD A NOTE.** `_tone` ends on an exponential ramp over
its whole length, so a "sustain" is a decay however long you make it; `_burst`
does not loop its 0.6s noise buffer, so anything longer plays silence for its
tail. Both are live bugs on twenty-seven shipped voices (CLAUDE.md §4.5, open
item 6) and neither is a relic build's to fix. So a sustain here is a
RE-STRIKE on a clock -- the spike storm's `chuff`, which exists for exactly
this reason and whose own comment is the argument: "phase-locked, the two
would fuse into a single buzz instead of reading as a turning thing".

So every candidate below is rendered as the WHOLE RUN it would make in a
fight, at its own cadence, for a full window's length. A single strike would
be the wrong question: what Rick has to judge is whether four seconds of it is
a presence or a nuisance.

RULE 3f, AND IT IS 5-FOR-5 AGAINST 0-FOR-4. Every candidate is an envelope
plus a rough band plus tones. None is a voice or a creature vocalisation --
that class has failed every time this project has tried it.

AND THEY ALL SIT LOW ON PURPOSE. `vesper-pass` lives at 470-1500 Hz and
`vesper-tip` at 880-2600 Hz, and those two are the only thing a viewer has to
learn from this ultimate. A hum in the same band masks the mechanic; these are
built to go UNDER it.

Rendered through `buildChain`, which is the path that ships, at a NON-ZERO
time, because an AudioParam whose first automation event is at t > 0 holds its
constructor default until then and a bench that renders at zero measures a
case the game cannot produce.

Writes one wav. Touches no build.
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
    ("1  DYNAMO",     0.24, "a machine under load — low sawtooth pair, fast "
                            "re-strike, the beam as a THING BEING POWERED"),
    ("2  GLASS RING", 0.62, "a struck bell held open — inharmonic triangles, "
                            "slow re-strike, the beam as LIGHT"),
    ("3  ARC CRACKLE",0.13, "electricity — short bandpassed noise ticks at "
                            "irregular spacing, the beam as something UNSTABLE"),
    ("4  FURNACE",    0.40, "air being burned — a wide low noise band with a "
                            "slow swell under it, the beam as HEAT"),
]

RENDER_JS = r"""async ([gap, secs, run]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);

  /* THE OPEN, played before every candidate so each one is heard ARRIVING the
     way it will in the fight -- a hum judged cold is judged in a context the
     game never produces. This is the shipped `vesper-open`. */
  const open = (t) => {
    B(t, { freq: 900, q: 0.8, gain: 0.20, dur: 0.09, type:"bandpass" });
    T(t, { freq: 210, to: 96, gain: 0.22, dur: 0.30, type:"sine" });
    T(t + 0.03, { freq: 784, to: 784, gain: 0.10, dur: 0.70, type:"triangle" });
    T(t + 0.05, { freq: 1176, to: 1176, gain: 0.05, dur: 0.62, type:"triangle" });
  };
  /* and a PASS partway through, so Rick can hear whether the hum buries the
     one event the viewer has to be able to pick out */
  const pass = (t) => {
    B(t, { freq: 1500, q: 1.1, gain: 0.09, dur: 0.07, type:"bandpass" });
    T(t, { freq: 470, to: 330, gain: 0.08, dur: 0.10, type:"triangle" });
  };
  const tip = (t) => {
    B(t, { freq: 2600, q: 1.6, gain: 0.20, dur: 0.05, type:"bandpass" });
    T(t, { freq: 880, to: 1480, gain: 0.16, dur: 0.16, type:"triangle" });
    T(t + 0.02, { freq: 1320, to: 1320, gain: 0.08, dur: 0.26, type:"sine" });
  };

  /* ONE STRIKE of each candidate. `n` is the strike index, so a candidate can
     vary across the run rather than repeating one sample -- which is the
     difference between a hum and a stutter. */
  const V = [];

  /* 1 — DYNAMO. Two sawtooths a fifth apart, re-struck fast enough that the
     decays overlap into a continuous floor. The slight detune between the
     pair is what stops it reading as a synth note. */
  V.push((t, n) => {
    const w = 1 + Math.sin(n * 0.7) * 0.012;
    T(t, { freq: 58 * w,  to: 54 * w, gain: 0.115, dur: 0.42, type:"sawtooth" });
    T(t, { freq: 87 * w,  to: 82 * w, gain: 0.055, dur: 0.38, type:"sawtooth" });
    T(t, { freq: 174 * w, to: 166 * w, gain: 0.022, dur: 0.30, type:"triangle" });
    if (n % 3 === 0)
      B(t, { freq: 260, q: 0.7, gain: 0.030, dur: 0.30, type:"lowpass" });
  });

  /* 2 — GLASS RING. Inharmonic partials, so it is a struck object and not a
     musical note, re-struck slowly enough that each one is heard as a strike.
     The one candidate that would still read at a low volume. */
  V.push((t, n) => {
    const w = 1 + ((n * 37) % 7 - 3) * 0.004;
    [[196,0.055,1.30],[293,0.038,1.15],[411,0.026,0.95],[607,0.015,0.75]]
      .forEach(([f,g,d]) => T(t, { freq: f*w, to: f*w*0.991, gain: g, dur: d,
                                   type:"triangle" }));
    T(t, { freq: 98*w, to: 92*w, gain: 0.070, dur: 0.55, type:"sine" });
    B(t, { freq: 3400, q: 1.6, gain: 0.020, dur: 0.030, type:"bandpass" });
  });

  /* 3 — ARC CRACKLE. Short noise ticks whose spacing WANDERS -- an even
     spacing at this rate is a buzz, and the wander is the whole character.
     Deterministic off `n`, no rng: two runs of the same clip must be
     bit-identical. */
  V.push((t, n) => {
    const j = ((n * 2654435761) % 1000) / 1000;
    const dt2 = (j - 0.5) * 0.055;
    B(t + dt2, { freq: 1100 + j * 900, q: 3.2, gain: 0.055 + j * 0.045,
                 dur: 0.035, type:"bandpass" });
    if (n % 2 === 0)
      T(t + dt2, { freq: 120 + j * 40, to: 70, gain: 0.045, dur: 0.10,
                   type:"sawtooth" });
    if (n % 7 === 0)
      B(t + dt2, { freq: 420, q: 0.9, gain: 0.070, dur: 0.16, type:"lowpass" });
  });

  /* 4 — FURNACE. A wide low band with a slow swell under it. The swell is a
     SECOND clock at a different period, so the two never line up and the
     result breathes instead of pulsing. */
  V.push((t, n) => {
    B(t, { freq: 300, q: 0.6, gain: 0.085, dur: 0.55, type:"lowpass" });
    B(t, { freq: 640, q: 0.8, gain: 0.030, dur: 0.45, type:"bandpass" });
    const sw = 0.5 + 0.5 * Math.sin(n * 0.51);
    T(t, { freq: 66, to: 50, gain: 0.045 + 0.045 * sw, dur: 0.60, type:"sine" });
    if (n % 5 === 0)
      B(t, { freq: 1800, q: 0.7, gain: 0.022, dur: 0.34, type:"highpass" });
  });

  const CAD = [0.24, 0.62, 0.13, 0.40];
  V.forEach((fn, i) => {
    const t0 = 1.0 + i * gap;
    open(t0);
    for (let k = 0; k * CAD[i] < run; k++) fn(t0 + 0.06 + k * CAD[i], k);
    /* two passes and a tip, at the measured rhythm, over the top */
    pass(t0 + 0.9); pass(t0 + 2.0); tip(t0 + 2.05); pass(t0 + 3.1);
  });

  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){ out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v; }
  return { pcm: out, sr, peak: +peak.toFixed(3) };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vesper.html")
    ap.add_argument("--gap", type=float, default=5.0)
    ap.add_argument("--run", type=float, default=3.6,
                    help="seconds of standing beam per candidate")
    ap.add_argument("--out",
                    default="../05-reference/v48-sentinel/hum-candidates.wav")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    secs = 1.0 + a.gap * len(CANDIDATES) + 2.0

    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RENDER_JS, [a.gap, secs, a.run])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(r["pcm"], dtype=np.float32)
    pcm = np.clip(d * 0.92 / max(1e-9, np.abs(d).max()), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(r["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    print(f"\n  {len(CANDIDATES)} candidates, {a.run:g}s of standing beam each, "
          f"one every {a.gap:g}s   (raw peak {r['peak']})")
    print(f"  Each one opens with the SHIPPED release voice and carries two "
          f"passes and a tip\n  over the top, so the question is not 'is this "
          f"a nice noise' but 'does four\n  seconds of it hold up, and can I "
          f"still hear the tip through it'.\n")
    for i, (name, cad, what) in enumerate(CANDIDATES):
        print(f"    {1.0 + i * a.gap:5.1f}s   {name:16} re-struck every "
              f"{cad:.2f}s   {what}")
    print(f"\n  wrote {out}")
    print("\n  NONE OF THESE IS WIRED IN. The hook is a `hum` clock in "
          "`tickSentinel`,\n  the same shape as the spike storm's `chuff`; "
          "the chosen voice goes into\n  vesper_build.py by hand.")


if __name__ == "__main__":
    main()
