#!/usr/bin/env python3
"""SIX CANDIDATE CAST SOUNDS, IN ONE FILE, FOR RICK TO PICK FROM.

    python3 cast_lab.py --out ../05-reference/v42/cast-candidates.wav

WHY THIS EXISTS. The cast voice took four cuts as a creature growl and every
one of them was a round trip: I write a sound I cannot hear, render a
25-second clip, Rick listens, Rick tells me it is wrong, I change an adjective.
Four of those cost most of a session.

The fix is not a better guess. It is to stop guessing SERIALLY. Everything
short and physical this session landed on the first attempt -- the lock, the
fork's split, the ballista string, the ratchet -- so the risk is not that any
one candidate is unbuildable, it is that I cannot tell which one Rick wants.
That is a question with six cheap answers, not one expensive one.

Each candidate is rendered through `buildChain`, which is the path that ships,
at a NON-ZERO time, because an AudioParam whose first automation event is at
t > 0 holds its constructor default until then and a bench that renders at zero
measures a case the game cannot produce.

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

# Every one is an ENVELOPE plus a rough band -- the class that has worked every
# time. No sustained voices; that class failed four times and the reason is
# structural, not a matter of effort.
CANDIDATES = [
    ("1  RATCHET & LOCK", "a siege engine loading — what is in the build now"),
    ("2  IRON CLAMP",     "one enormous clack, long inharmonic ring-out"),
    ("3  PNEUMATIC SLAM", "a pressure release, then a hard stop"),
    ("4  STRUCK BELL",    "a single toll, inharmonic, ominous, sustains"),
    ("5  DRAW & LOCK",    "metal rasping out of a housing, then a catch"),
    ("6  SPOOL UP",       "an impact, then a rising whine — something going live"),
]

# Rick picked 2 and asked for "lower and louder". LOWER is the word that
# produced a growl 97.7% under 60 Hz that no laptop could reproduce, so this
# offers three DEPTHS rather than one guess -- the same reason the six above
# exist. `drop` scales every partial and the thump; `push` is the level.
CLAMPS = [
    ("2a  A LITTLE LOWER", 0.80, 1.30, "ring at 168/254/366/537 Hz"),
    ("2b  CLEARLY LOWER",  0.66, 1.34, "ring at 139/209/302/443 Hz"),
    ("2c  VERY LOW",       0.55, 1.38, "ring at 116/174/252/369 Hz — near the "
                                       "floor a laptop can play"),
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

  const V = [];

  /* 1 — RATCHET & LOCK */
  V.push((t) => {
    B(t, { freq: 3600, q: 0.7, gain: 0.30, dur: 0.035, type:"highpass" });
    B(t, { freq: 700,  q: 1.4, gain: 0.24, dur: 0.09,  type:"bandpass" });
    T(t, { freq: 96, to: 34,   gain: 0.30, dur: 0.30,  type:"sine" });
    for (let i = 0; i < 7; i++){
      const d = 0.055 + i * 0.030 + i * i * 0.006;
      B(t + d, { freq: 2400 - i * 90, q: 2.2, gain: 0.115 - i * 0.012,
                 dur: 0.028, type:"bandpass" });
    }
    T(t + 0.06, { freq: 132, to: 118, gain: 0.10,  dur: 1.15, type:"triangle" });
    T(t + 0.06, { freq: 197, to: 176, gain: 0.055, dur: 1.05, type:"triangle" });
    B(t + 0.40, { freq: 520, q: 0.8,  gain: 0.07,  dur: 0.55, type:"lowpass" });
  });

  /* 2 — IRON CLAMP. One event, and the whole character is in the ring. */
  V.push((t) => {
    B(t, { freq: 5200, q: 0.7, gain: 0.30, dur: 0.030, type:"highpass" });
    B(t, { freq: 900,  q: 1.2, gain: 0.30, dur: 0.12,  type:"bandpass" });
    T(t, { freq: 140, to: 58,  gain: 0.34, dur: 0.50,  type:"sine" });
    /* inharmonic partials -- integer ratios would be a musical note, and a
       clamp is not a note */
    [[210,0.085,1.9],[317,0.065,1.7],[458,0.045,1.5],[671,0.028,1.2]]
      .forEach(([f,g,d]) => T(t + 0.008, { freq: f, to: f*0.985, gain: g,
                                           dur: d, type:"triangle" }));
  });

  /* 3 — PNEUMATIC SLAM. The hiss is the wind-up; the stop is the trigger. */
  V.push((t) => {
    B(t,        { freq: 1800, q: 0.6, gain: 0.11, dur: 0.30, type:"highpass" });
    B(t + 0.22, { freq: 620,  q: 1.6, gain: 0.32, dur: 0.09, type:"bandpass" });
    B(t + 0.22, { freq: 4200, q: 0.8, gain: 0.20, dur: 0.04, type:"highpass" });
    T(t + 0.22, { freq: 124, to: 38,  gain: 0.32, dur: 0.38, type:"sine" });
    B(t + 0.30, { freq: 3600, q: 0.7, gain: 0.055, dur: 0.40, type:"highpass" });
  });

  /* 4 — STRUCK BELL. Sustains, which no other cast voice here does. */
  V.push((t) => {
    B(t, { freq: 6200, q: 0.8, gain: 0.17, dur: 0.035, type:"highpass" });
    [[86,0.12,2.4],[172,0.10,2.2],[205,0.075,2.0],[258,0.055,1.8],
     [341,0.035,1.5],[512,0.022,1.1]]
      .forEach(([f,g,d]) => T(t, { freq: f, to: f*0.992, gain: g, dur: d,
                                   type: f < 200 ? "sine" : "triangle" }));
    T(t, { freq: 118, to: 44, gain: 0.20, dur: 0.45, type:"sine" });
  });

  /* 5 — DRAW & LOCK. A rasp with a destination. */
  V.push((t) => {
    B(t,        { freq: 1500, q: 0.8, gain: 0.13, dur: 0.30, type:"bandpass" });
    B(t + 0.02, { freq: 2100, q: 1.0, gain: 0.09, dur: 0.28, type:"bandpass" });
    B(t + 0.30, { freq: 4400, q: 0.8, gain: 0.27, dur: 0.035, type:"highpass" });
    B(t + 0.30, { freq: 640,  q: 1.4, gain: 0.24, dur: 0.10, type:"bandpass" });
    T(t + 0.30, { freq: 112, to: 40,  gain: 0.30, dur: 0.34, type:"sine" });
    T(t + 0.31, { freq: 246, to: 232, gain: 0.05, dur: 0.9,  type:"triangle" });
  });

  /* 6 — SPOOL UP. The only one that RISES, so it promises rather than states. */
  V.push((t) => {
    B(t, { freq: 3000, q: 0.7, gain: 0.28, dur: 0.04, type:"highpass" });
    T(t, { freq: 90, to: 30,   gain: 0.30, dur: 0.28, type:"sine" });
    T(t + 0.02, { freq: 180, to: 540, gain: 0.10,  dur: 0.95, type:"sawtooth" });
    T(t + 0.02, { freq: 271, to: 812, gain: 0.048, dur: 0.95, type:"sawtooth" });
    B(t + 0.05, { freq: 900, q: 0.7, gain: 0.085, dur: 0.85, type:"lowpass" });
  });

  /* THE CLAMP, AT THREE DEPTHS. `drop` scales the thump, the clack body and
     every ring partial together, so the whole object gets bigger rather than
     just darker; `push` is the level. The 5.2kHz tick is scaled far less than
     everything else -- it is the metal-on-metal contact and it is what stops a
     lower clamp reading as a cardboard box. */
  const CL = [[0.80,1.30],[0.66,1.34],[0.55,1.38]];
  const clamp = (t, drop, push) => {
    B(t, { freq: 5200 * (0.55 + 0.45*drop), q: 0.7, gain: 0.30*push,
           dur: 0.030, type:"highpass" });
    B(t, { freq: 900 * drop, q: 1.2, gain: 0.30*push, dur: 0.13, type:"bandpass" });
    T(t, { freq: 140*drop, to: 58*drop, gain: 0.34*push, dur: 0.55, type:"sine" });
    [[210,0.085,2.3],[317,0.065,2.1],[458,0.045,1.8],[671,0.028,1.4]]
      .forEach(([f,g,d]) => T(t + 0.008, { freq: f*drop, to: f*drop*0.985,
                                           gain: g*push, dur: d, type:"triangle" }));
  };
  if (mode === "clamp"){
    CL.forEach(([drop, push], i) => clamp(1.0 + i * gap, drop, push));
  } else {
    V.forEach((fn, i) => fn(1.0 + i * gap));
  }
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
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw-frame.html")
    ap.add_argument("--gap", type=float, default=2.6)
    ap.add_argument("--clamp", action="store_true",
                    help="three depths of candidate 2 instead of the six")
    ap.add_argument("--out", default="../05-reference/v42/cast-candidates.wav")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = CLAMPS if a.clamp else CANDIDATES
    secs = 1.0 + a.gap * len(rows) + 2.0

    with game(game_path=gp) as (page, errors):
        r = page.evaluate(RENDER_JS, [a.gap, secs,
                                      "clamp" if a.clamp else "six"])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(r["pcm"], dtype=np.float32)
    pcm = np.clip(d * 0.92 / max(1e-9, np.abs(d).max()), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(r["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    print(f"\n  {len(rows)} candidates, one every {a.gap:g}s, "
          f"first at 1.0s   (raw peak {r['peak']})\n")
    for i, row in enumerate(rows):
        name = row[0]; what = row[-1]
        print(f"    {1.0 + i * a.gap:5.1f}s   {name:20} {what}")
    print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
