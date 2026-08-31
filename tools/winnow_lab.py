#!/usr/bin/env python3
"""THE WINNOWING'S VOICE, AS A SPREAD, BEFORE ANYBODY IS ASKED ANYTHING.

    python winnow_lab.py --out ../05-reference/v47/winnow-cast.wav
    python winnow_lab.py --rung --out ../05-reference/v47/winnow-rung.wav

WHY A SPREAD. v42 wrote the cast voice four times as four serial guesses and
every one cost a round trip: write a sound I cannot hear, render a clip, Rick
listens, Rick says it is wrong, I change an adjective. v43 spread first and the
Stasis Field's voice landed in ONE round trip. §3 rule 2: the trade named, and
priced from measurement wherever a measurement can price it.

THIS ULTIMATE HAS TWO VOICES AND THEY HAVE OPPOSITE PROBLEMS.

    THE CAST fires 2.4 times a fight and has to HAND OVER: the window is four
    seconds long and every other cast in this game is an event that ends. Only
    the Stasis Field has had to do this before.

    THE RUNG fires about ten times a cast — measured, not guessed: 55% of
    kunai reach the top rung, which is 38 a cast, and the sound and the
    director's beat share one 0.4s gate to keep it from becoming a wash. So it
    has to survive being heard ten times in four seconds, which is the
    opposite constraint from the cast's.

Each candidate is rendered through `buildChain` — the path that ships — at a
NON-ZERO time, because an AudioParam whose first automation event is at t > 0
holds its constructor default until then, and a bench that renders at zero
measures a case the game cannot produce.

AND EVERY ONE IS INSIDE THE ENVELOPE OF TWO KNOWN BUGS. `_burst` does not loop
its 0.6s noise buffer, so no burst here is longer than that; `_tone` ends on an
exponential ramp over its whole length, so nothing here is HELD — anything that
must last is re-struck. Both bugs are live on twenty-six shipped voices and
fixing either is chain-wide and Rick's.

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

CASTS = [
    ("1  SHEAR",        "metal shearing, a body falling away, then the stream "
                        "— what is in the build now"),
    ("2  SCATTER",      "a handful of hard blades thrown at once, then the "
                        "hiss of them leaving"),
    ("3  GUST",         "the hall filling — a rising band of air that breaks "
                        "into the stream"),
    ("4  SPRING",       "the blades coming off under tension: a wound creak, "
                        "then a release"),
]

RUNGS = [
    ("a  CHIME",  "a small rising bell — what is in the build now"),
    ("b  GLINT",  "a glassy tick with an upward bend, no note in it"),
    ("c  KNOCK",  "a dry wooden knock, pitched by rung but not musical"),
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

  /* ---- THE CAST, four registers ------------------------------------- */
  const V = [];

  /* 1 — SHEAR. One object becoming seventy: a top that shears, a body that
     falls away under it, and then four airy re-strikes at roughly the volley
     cadence so the sound hands over to the window instead of ending. */
  V.push((t) => {
    B(t, { freq: 3400, q: 1.4, gain: 0.26, dur: 0.055, type:"bandpass" });
    T(t, { freq: 1250, to: 240, gain: 0.20, dur: 0.16, type:"sawtooth" });
    B(t + 0.015, { freq: 1500, q: 0.7, gain: 0.15, dur: 0.30, type:"bandpass" });
    [[0.10,0.085],[0.42,0.075],[0.75,0.062],[1.06,0.048]].forEach(([d,g]) => {
      B(t + d, { freq: 2600, q: 0.9, gain: g, dur: 0.24, type:"bandpass" });
      T(t + d, { freq: 620, to: 470, gain: g * 0.55, dur: 0.26, type:"triangle" });
    });
  });

  /* 2 — SCATTER. The event is MANY, not one. Eleven hard ticks inside 90ms,
     irregularly spaced and falling in pitch, then the hiss of them leaving.
     The risk this one takes is that a crowd of transients reads as a rattle
     rather than as a weapon. */
  V.push((t) => {
    for (let i = 0; i < 11; i++){
      const d = i * 0.008 + (i % 3) * 0.004;
      B(t + d, { freq: 3900 - i * 190, q: 2.6, gain: 0.16 - i * 0.008,
                 dur: 0.022, type:"bandpass" });
    }
    T(t, { freq: 300, to: 96, gain: 0.26, dur: 0.22, type:"square" });
    B(t + 0.05, { freq: 2200, q: 0.6, gain: 0.13, dur: 0.42, type:"highpass" });
    [[0.36,0.070],[0.68,0.058],[1.00,0.044]].forEach(([d,g]) =>
      B(t + d, { freq: 3000, q: 0.8, gain: g, dur: 0.26, type:"bandpass" }));
  });

  /* 3 — GUST. The one candidate whose ATTACK is not an impact: a band of air
     that swells for a third of a second and then breaks. It is the only one
     that says "the hall is filling" rather than "something was thrown", and
     it is the one most likely to be inaudible under an ultimate's own
     particle field. Offered because being wrong about the register is what
     costs, and a spread with no soft option cannot reveal it. */
  V.push((t) => {
    [[0.00,900,0.055],[0.08,1400,0.075],[0.16,2000,0.095],[0.24,2600,0.115]]
      .forEach(([d,f,g]) => B(t + d, { freq: f, q: 0.5, gain: g, dur: 0.30,
                                       type:"bandpass" }));
    B(t + 0.30, { freq: 4200, q: 0.8, gain: 0.20, dur: 0.05, type:"highpass" });
    T(t + 0.30, { freq: 520, to: 210, gain: 0.14, dur: 0.20, type:"triangle" });
    [[0.42,0.080],[0.74,0.066],[1.06,0.050]].forEach(([d,g]) => {
      B(t + d, { freq: 2400, q: 0.7, gain: g, dur: 0.28, type:"bandpass" });
      T(t + d, { freq: 470, to: 380, gain: g * 0.5, dur: 0.28, type:"triangle" });
    });
  });

  /* 4 — SPRING. The blades come off under tension. A short wound creak — a
     rising rasp made of re-struck ticks rather than a held tone — and then a
     release with a real bottom to it. */
  V.push((t) => {
    for (let i = 0; i < 8; i++)
      B(t + i * 0.026, { freq: 700 + i * 210, q: 3.0, gain: 0.055,
                         dur: 0.030, type:"bandpass" });
    B(t + 0.22, { freq: 5000, q: 0.8, gain: 0.24, dur: 0.04, type:"highpass" });
    B(t + 0.22, { freq: 820, q: 1.2, gain: 0.22, dur: 0.11, type:"bandpass" });
    T(t + 0.22, { freq: 190, to: 62, gain: 0.30, dur: 0.30, type:"sine" });
    [[0.44,0.072],[0.76,0.060],[1.08,0.046]].forEach(([d,g]) => {
      B(t + d, { freq: 2700, q: 0.9, gain: g, dur: 0.24, type:"bandpass" });
      T(t + d, { freq: 560, to: 430, gain: g * 0.5, dur: 0.26, type:"triangle" });
    });
  });

  /* ---- THE RUNG, three registers ------------------------------------- */
  /* EACH ONE IS PLAYED FOUR TIMES, 0.42s APART, because that is what it
     actually sounds like: the gate is 0.4s and a cast fires ten of them. A
     rung voice judged once is judged in a condition the game never produces. */
  const R = [];
  R.push((t, n) => {                                   // a — CHIME
    const f = 640 * Math.pow(1.26, n);
    T(t, { freq: f, to: f * 0.86, gain: 0.055, dur: 0.13, type:"triangle" });
    B(t, { freq: f * 2.4, q: 2.2, gain: 0.035, dur: 0.045, type:"bandpass" });
  });
  R.push((t, n) => {                                   // b — GLINT
    const f = 2600 + n * 420;
    B(t, { freq: f, q: 3.4, gain: 0.055, dur: 0.026, type:"bandpass" });
    T(t, { freq: f * 0.42, to: f * 0.60, gain: 0.030, dur: 0.07, type:"sine" });
  });
  R.push((t, n) => {                                   // c — KNOCK
    const f = 240 + n * 55;
    B(t, { freq: f * 3.2, q: 1.6, gain: 0.045, dur: 0.030, type:"bandpass" });
    T(t, { freq: f, to: f * 0.55, gain: 0.055, dur: 0.075, type:"triangle" });
  });

  if (mode === "rung"){
    R.forEach((fn, i) => {
      const t0 = 1.0 + i * gap;
      /* rungs 1..3 and then 3 again — the order a cast produces */
      [1, 2, 3, 3].forEach((n, k) => fn(t0 + k * 0.42, n));
    });
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
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--gap", type=float, default=0.0)
    ap.add_argument("--rung", action="store_true",
                    help="the three rung voices instead of the four casts")
    ap.add_argument("--out", default="../05-reference/v47/winnow-cast.wav")
    a = ap.parse_args()

    rows = RUNGS if a.rung else CASTS
    gap = a.gap or (2.6 if a.rung else 3.0)
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    secs = 1.0 + gap * len(rows) + 2.0

    with game(game_path=resolve_game(a.game)) as (page, errors):
        r = page.evaluate(RENDER_JS, [gap, secs, "rung" if a.rung else "cast"])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(r["pcm"], dtype=np.float32)
    # NORMALISED FOR AUDITION AND NOT FOR THE GAME. The relative levels inside
    # one candidate are the shipping ones; the level BETWEEN candidates is not
    # a thing this file is asking about, and a quiet candidate losing a
    # comparison for being quiet is v42 §3c's trap.
    pcm = np.clip(d * 0.92 / max(1e-9, float(np.abs(d).max())), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(r["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    print(f"\n  {len(rows)} candidates, one every {gap:g}s, first at 1.0s"
          f"   (raw peak {r['peak']})\n")
    for i, (name, what) in enumerate(rows):
        print(f"    {1.0 + i * gap:5.1f}s   {name:14} {what}")
    if a.rung:
        print("\n    each one is struck FOUR TIMES, 0.42s apart, at rungs "
              "1/2/3/3 —\n    which is the density a real cast produces")
    print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
