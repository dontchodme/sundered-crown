#!/usr/bin/env python3
"""CANDIDATE SOUNDS FOR THE STASIS FIELD, IN ONE FILE, FOR RICK TO PICK FROM.

    python3 field_lab.py --out ../05-reference/v43/field-cast-candidates.wav
    python3 field_lab.py --hold --out ../05-reference/v43/field-hold-candidates.wav

v42's lesson, applied at the front instead of after four failures: when the
judge is a person and the author cannot hear, a candidate costs nothing and a
round trip costs everything. The cast voice took four serial cuts to fail and
two spreads to land.

AND THE CLASS DISCIPLINE HOLDS. Impacts, latches, ratchets, springs, whooshes,
fire, stone and metal resonance are five for five in this project; sustained
biological voices are nought for four and are not attempted. Every candidate
below is an envelope plus a rough band plus tones.

ONE CONSTRAINT THAT IS NOT TASTE. `_burst` does not loop its 0.6s noise buffer
(v42 §12), so every burst here is under 0.6s; a longer one plays silence for
its tail and would be measured as a sound that fades early. And `_tone` ends on
an exponential ramp to 0.0001 over its whole length, so a HELD note does not
exist in this toolkit -- anything that has to last is re-struck.

Rendered through `buildChain`, which is the path that ships, at a NON-ZERO
time, because an AudioParam whose first automation event is at t > 0 holds its
constructor default until then.

Writes one wav. Touches no build.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

CASTS = [
    ("1  ARC STRIKE & HUM", "what is in the build now — a snap, then a field "
                            "that buzzes four times"),
    ("2  CAPACITOR CHARGE", "a rising whine INTO the snap: it promises, then "
                            "delivers"),
    ("3  TESLA COIL",       "no tone at all — a train of hard discharges that "
                            "slows into a rhythm"),
    ("4  CONTACTOR CLOSE",  "a deep mains buzz that fades UP, then a heavy "
                            "industrial clunk on top"),
    ("5  GLASS & FIELD",    "a bright inharmonic ring decaying into a low "
                            "hum — cold and clean, not industrial"),
    ("6  PRESSURE DROP",    "a swept whoosh downward, a bass thud, then a "
                            "shimmer — the air changes"),
]

HOLDS = [
    ("A  IRON CLAMP",  "what is in the build now — bright tick, short body, "
                       "drop, no ring at all"),
    ("B  GLASS SEIZE", "a high shattering tick cut off mid-decay, over a very "
                       "short sub"),
    ("C  DEAD STOP",   "a heavy thud with the tail gated hard — everything "
                       "ceasing at once"),
    ("D  CRYSTAL LOCK", "a bright ping that is CUT rather than allowed to ring, "
                        "plus a low click"),
]

RENDER_JS = r"""async ([gap, secs, mode]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);

  const C = [];

  /* 1 — ARC STRIKE & HUM. The shipped one. */
  C.push((t) => {
    B(t, { freq: 5400, q: 0.9, gain: 0.30, dur: 0.05, type:"highpass" });
    T(t, { freq: 1500, to: 190, gain: 0.20, dur: 0.15, type:"square" });
    B(t + 0.02, { freq: 900, q: 0.8, gain: 0.14, dur: 0.28, type:"bandpass" });
    [[0.05,0.165],[0.41,0.150],[0.80,0.128],[1.14,0.104]].forEach(([d,g]) => {
      T(t + d,         { freq: 108, to: 104, gain: g,        dur: 0.50, type:"sawtooth" });
      T(t + d + 0.004, { freq: 162, to: 158, gain: g * 0.55, dur: 0.46, type:"triangle" });
      T(t + d + 0.008, { freq: 324, to: 316, gain: g * 0.34, dur: 0.40, type:"triangle" });
    });
    [[0.22,4200],[0.58,2800],[0.95,3600],[1.30,2400]].forEach(([d,hz]) =>
      B(t + d, { freq: hz, q: 1.6, gain: 0.075, dur: 0.06, type:"bandpass" }));
  });

  /* 2 — CAPACITOR CHARGE. The only one that arrives at its own snap. */
  C.push((t) => {
    T(t, { freq: 220, to: 1900, gain: 0.10, dur: 0.42, type:"sawtooth" });
    T(t + 0.01, { freq: 331, to: 2850, gain: 0.05, dur: 0.42, type:"sawtooth" });
    B(t + 0.05, { freq: 2400, q: 0.6, gain: 0.05, dur: 0.38, type:"highpass" });
    B(t + 0.42, { freq: 6000, q: 0.8, gain: 0.34, dur: 0.04, type:"highpass" });
    B(t + 0.42, { freq: 760,  q: 1.2, gain: 0.28, dur: 0.10, type:"bandpass" });
    T(t + 0.42, { freq: 150, to: 46,  gain: 0.32, dur: 0.34, type:"sine" });
    [[0.46,0.150],[0.83,0.120],[1.18,0.092]].forEach(([d,g]) => {
      T(t + d,         { freq: 110, to: 106, gain: g,        dur: 0.48, type:"sawtooth" });
      T(t + d + 0.006, { freq: 330, to: 322, gain: g * 0.32, dur: 0.40, type:"triangle" });
    });
  });

  /* 3 — TESLA COIL. No tone anywhere. Rate is the whole character. */
  C.push((t) => {
    for (let i = 0; i < 16; i++){
      const d = i * (0.028 + i * 0.0075);
      if (d > 1.5) break;
      const hz = 5200 - i * 130 + (i % 3) * 700;
      B(t + d, { freq: hz, q: 1.1 + (i % 4) * 0.5,
                 gain: (0.30 - i * 0.013) * (i % 2 ? 0.72 : 1),
                 dur: 0.030, type:"bandpass" });
      if (i % 2 === 0)
        B(t + d, { freq: 620, q: 1.0, gain: 0.10 - i * 0.005, dur: 0.05, type:"lowpass" });
    }
    T(t, { freq: 128, to: 44, gain: 0.24, dur: 0.30, type:"sine" });
  });

  /* 4 — CONTACTOR CLOSE. The hum arrives BEFORE the event, which no other
     cast voice in the game does. */
  C.push((t) => {
    /* a fade-UP faked out of four re-strikes of rising level, because `_tone`
       only ever decays */
    [[0.00,0.030],[0.13,0.055],[0.26,0.095],[0.39,0.150]].forEach(([d,g]) => {
      T(t + d,         { freq: 60,  to: 59,  gain: g,        dur: 0.22, type:"sawtooth" });
      T(t + d + 0.004, { freq: 120, to: 118, gain: g * 0.62, dur: 0.20, type:"triangle" });
      T(t + d + 0.008, { freq: 240, to: 236, gain: g * 0.28, dur: 0.18, type:"triangle" });
    });
    B(t + 0.52, { freq: 3400, q: 0.9, gain: 0.28, dur: 0.04, type:"highpass" });
    B(t + 0.52, { freq: 420,  q: 0.9, gain: 0.32, dur: 0.14, type:"lowpass" });
    T(t + 0.52, { freq: 104, to: 40,  gain: 0.34, dur: 0.40, type:"sine" });
    [[0.56,0.135],[0.92,0.105],[1.26,0.078]].forEach(([d,g]) => {
      T(t + d,         { freq: 60,  to: 59,  gain: g,        dur: 0.44, type:"sawtooth" });
      T(t + d + 0.006, { freq: 240, to: 236, gain: g * 0.30, dur: 0.38, type:"triangle" });
    });
  });

  /* 5 — GLASS & FIELD. Cold, and the only candidate with no noise in its
     attack -- so it reads as arcane rather than as machinery. */
  C.push((t) => {
    B(t, { freq: 7200, q: 1.0, gain: 0.13, dur: 0.025, type:"highpass" });
    [[523,0.115,1.5],[791,0.085,1.3],[1187,0.055,1.1],[1613,0.032,0.9]]
      .forEach(([f,g,d]) => T(t, { freq: f, to: f*0.994, gain: g, dur: d,
                                   type:"triangle" }));
    T(t + 0.02, { freq: 175, to: 62, gain: 0.26, dur: 0.42, type:"sine" });
    [[0.30,0.115],[0.70,0.095],[1.08,0.072]].forEach(([d,g]) => {
      T(t + d,         { freq: 131, to: 128, gain: g,        dur: 0.52, type:"triangle" });
      T(t + d + 0.006, { freq: 262, to: 256, gain: g * 0.42, dur: 0.46, type:"sine" });
      T(t + d + 0.012, { freq: 393, to: 384, gain: g * 0.20, dur: 0.40, type:"triangle" });
    });
  });

  /* 6 — PRESSURE DROP. A whoosh down, a thud, then a shimmer. */
  C.push((t) => {
    B(t,        { freq: 3800, q: 0.5, gain: 0.16, dur: 0.14, type:"bandpass" });
    B(t + 0.10, { freq: 1700, q: 0.5, gain: 0.20, dur: 0.14, type:"bandpass" });
    B(t + 0.20, { freq: 700,  q: 0.6, gain: 0.24, dur: 0.16, type:"bandpass" });
    B(t + 0.34, { freq: 340,  q: 0.7, gain: 0.30, dur: 0.16, type:"lowpass" });
    T(t + 0.34, { freq: 118, to: 34,  gain: 0.36, dur: 0.46, type:"sine" });
    [[0.42,3100],[0.66,4300],[0.94,2600],[1.24,3700]].forEach(([d,hz]) =>
      B(t + d, { freq: hz, q: 2.6, gain: 0.055, dur: 0.09, type:"bandpass" }));
    [[0.44,0.085],[0.86,0.062]].forEach(([d,g]) => {
      T(t + d,         { freq: 96,  to: 94,  gain: g,        dur: 0.50, type:"sawtooth" });
      T(t + d + 0.006, { freq: 288, to: 282, gain: g * 0.30, dur: 0.42, type:"triangle" });
    });
  });

  const H = [];

  /* A — IRON CLAMP. The shipped one. */
  H.push((t) => {
    B(t, { freq: 4400, q: 1.2, gain: 0.32, dur: 0.035, type:"bandpass" });
    B(t, { freq: 560,  q: 0.8, gain: 0.28, dur: 0.10,  type:"lowpass" });
    B(t + 0.01, { freq: 3000, q: 2.0, gain: 0.10, dur: 0.12, type:"bandpass" });
    T(t, { freq: 320, to: 74, gain: 0.34, dur: 0.18, type:"square" });
    T(t + 0.02, { freq: 92, to: 88, gain: 0.20, dur: 0.30, type:"sine" });
  });

  /* B — GLASS SEIZE. */
  H.push((t) => {
    B(t, { freq: 8000, q: 0.8, gain: 0.26, dur: 0.030, type:"highpass" });
    [[1450,0.10,0.10],[2190,0.075,0.085],[3310,0.05,0.07]]
      .forEach(([f,g,d]) => T(t, { freq: f, to: f*0.97, gain: g, dur: d,
                                   type:"triangle" }));
    T(t, { freq: 210, to: 66, gain: 0.30, dur: 0.16, type:"sine" });
    B(t + 0.015, { freq: 900, q: 1.6, gain: 0.16, dur: 0.055, type:"bandpass" });
  });

  /* C — DEAD STOP. The heaviest, and the shortest. */
  H.push((t) => {
    B(t, { freq: 2600, q: 1.0, gain: 0.20, dur: 0.022, type:"bandpass" });
    B(t, { freq: 300,  q: 0.7, gain: 0.36, dur: 0.075, type:"lowpass" });
    T(t, { freq: 150, to: 42, gain: 0.40, dur: 0.13, type:"sine" });
    T(t + 0.005, { freq: 76, to: 70, gain: 0.26, dur: 0.19, type:"sine" });
  });

  /* D — CRYSTAL LOCK. A ping that is not allowed to finish. */
  H.push((t) => {
    B(t, { freq: 6400, q: 1.2, gain: 0.22, dur: 0.028, type:"bandpass" });
    [[988,0.13,0.13],[1482,0.09,0.11],[2470,0.05,0.085]]
      .forEach(([f,g,d]) => T(t, { freq: f, to: f*0.99, gain: g, dur: d,
                                   type:"sine" }));
    B(t + 0.10, { freq: 480, q: 1.1, gain: 0.20, dur: 0.06, type:"bandpass" });
    T(t + 0.10, { freq: 118, to: 52, gain: 0.26, dur: 0.20, type:"sine" });
  });

  const V = mode === "hold" ? H : C;
  V.forEach((fn, i) => fn(1.0 + i * gap));
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
    ap.add_argument("--game", default="../02-chain/sc-paradox-hold-clamp.html")
    ap.add_argument("--gap", type=float, default=2.8)
    ap.add_argument("--hold", action="store_true",
                    help="the four hold sounds instead of the six casts")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    rows = HOLDS if a.hold else CASTS
    gap = 1.8 if a.hold else a.gap
    default = ("field-hold-candidates.wav" if a.hold
               else "field-cast-candidates.wav")
    out = (HERE / (a.out or f"../05-reference/v43/{default}")).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    secs = 1.0 + gap * len(rows) + 2.5

    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RENDER_JS, [gap, secs, "hold" if a.hold else "cast"])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(r["pcm"], dtype=np.float32)
    pcm = np.clip(d * 0.92 / max(1e-9, np.abs(d).max()), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(r["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    print(f"\n  {len(rows)} candidates, one every {gap:g}s, first at 1.0s   "
          f"(raw peak {r['peak']})\n")
    for i, (name, what) in enumerate(rows):
        print(f"    {1.0 + i * gap:5.1f}s   {name:22} {what}")
    print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
