#!/usr/bin/env python
"""SCOUR'S VOICE, AS A SPREAD, BEFORE ANYBODY IS ASKED ANYTHING.

    python scour_sound_lab.py --game ../02-chain/sc-vortex.html

Brief stage 5: "Sound -- Rick has no preference (2026-09-02). Render a spread,
as v43 did: three casts x three holds x two tick voices, in one sheet, and ask
him. A starting register: cast = rising wind into a peak; hold = continuous wind
with crackle; tick = a short dry zap. DO NOT SHIP THE FIRST ONE BUILT."

WHY A SPREAD AND NOT A GUESS. v42 spread after four serial failures; v43 spread
FIRST and the sound landed in one round trip -- six casts and four holds
rendered before Rick was asked anything, and the answer was "first option on
both". CLAUDE.md rule 2: being wrong about the REGISTER is what costs, and a
spread of one can never reveal it.

WHAT SCOUR NEEDS THAT NO OTHER RELIC IN THIS GAME HAS NEEDED. Every other
ultimate's voice is an EVENT -- a strike, a nova, a shatter. This one has to
hold for TEN SECONDS and carry seven ticks a second under it, which is 70 ticks
a window. So the three questions are separable and this sheet asks them
separately:

    A. THE CAST     does the window OPEN? one event, 8 of them a fight
    B. THE HOLD     does ten seconds of it wear out? and does it leave room?
    C. THE TICK     at SEVEN A SECOND, is it a grind or is it a buzz?

AND THE HOLD HAS TO BE RE-STRUCK, WHICH IS NOT A STYLE CHOICE. CLAUDE.md 4.5:
`_burst` does not loop its 0.6s noise buffer, so anything longer plays silence
for its tail, and `_tone` ends on an exponential ramp over its whole length --
**a held note does not exist in this toolkit.** Every hold below is struck
repeatedly at its own cadence, and the cadence IS the character.

NOTHING HERE IS WIRED IN. `SFX.play("ult", …)` currently falls through the whole
relic dispatch to the final `else` -- the RUNE-CRACK, a half-second burst
written for runic -- so Scour is announced by another school's sound and then
goes quiet for ten seconds. The chosen voice goes into `duskreave_build.py` by
hand, the way Vesper's did.
"""
from __future__ import annotations
import argparse, pathlib, sys, wave

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game, resolve_game  # noqa: E402

CASTS = [
    ("A1  UPDRAFT", "noise sweeping UP through its cutoff into a low boom -- "
                    "the brief's own register, air being pulled off the floor"),
    ("A2  RIFT",    "a hard crack and a detuned pair falling away under it -- "
                    "the hall tearing open rather than the wind arriving"),
    ("A3  INHALE",  "a quiet swell that snaps and DROPS into the hold -- the "
                    "one that promises a window rather than announcing a hit"),
]
HOLDS = [
    ("B1  WIND",    "wide bandpassed noise re-struck every 0.26s, cutoff "
                    "wandering slowly -- the literal reading of the brief"),
    ("B2  TURBINE", "a low sawtooth pair re-struck fast enough that the decays "
                    "overlap into a floor -- a MACHINE, not weather"),
    ("B3  HOLLOW",  "a sparse low drone with a tuned resonance -- the quietest, "
                    "and the one that leaves the most room for the ticks"),
]
TICKS = [
    ("C1  ZAP",     "a short dry bandpassed tick, 30ms -- the brief's register"),
    ("C2  BITE",    "a transient with a pitched blip on it, so seven a second "
                    "reads as a RATE rather than as a texture"),
]

WOOSH_JS = r"""async ([secs]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  const B = (t, o) => S._burst(t, o);

  const W = (t, o) => S._sweep(t, o);
  /* W1 -- THE OLD ONE, five `_burst`s at rising frequencies. Kept as the
     CONTROL, because it is what Rick heard and called ticks, and a spread
     with nothing wrong in it cannot show that the new one is better. */
  const woosh = (t, n) => {
    const base = 360 + (n % 3) * 85;
    [[0.00,1.00,0.048],[0.07,2.05,0.066],[0.15,3.30,0.060],
     [0.25,2.30,0.042],[0.35,1.25,0.026]].forEach(([d,k,g]) =>
      B(t + d, { freq: base * k, q: 0.50, gain: g, dur: 0.30,
                 type:"bandpass" }));
    B(t + 0.10, { freq: 150, q: 0.5, gain: 0.030, dur: 0.42, type:"lowpass" });
  };
  /* W3 -- THE SHIPPED ONE NOW: `_sweep`, up then down, low Q. */
  const wooshSwept = (t, n) => {
    const v = 1 + (n % 3) * 0.11;
    W(t, { f0: 240*v, f1: 1650*v, q: 0.55, gain: 0.105, dur: 0.34,
           atk: 0.20, type:"bandpass" });
    W(t + 0.26, { f0: 1500*v, f1: 300*v, q: 0.55, gain: 0.078, dur: 0.40,
                  atk: 0.10, type:"bandpass" });
    W(t + 0.05, { f0: 120, f1: 260, q: 0.5, gain: 0.055, dur: 0.46,
                  atk: 0.22, type:"lowpass" });
  };
  /* W4 -- SLOWER AND DEEPER. The same construction with a longer, lower pass,
     for the case where W3 is right in kind but too brisk. */
  const wooshSlow = (t, n) => {
    const v = 1 + (n % 3) * 0.09;
    W(t, { f0: 170*v, f1: 1150*v, q: 0.48, gain: 0.115, dur: 0.52,
           atk: 0.30, type:"bandpass" });
    W(t + 0.40, { f0: 1050*v, f1: 210*v, q: 0.48, gain: 0.085, dur: 0.56,
                  atk: 0.16, type:"bandpass" });
    W(t + 0.06, { f0: 100, f1: 220, q: 0.5, gain: 0.065, dur: 0.58,
                  atk: 0.30, type:"lowpass" });
  };

  /* A WIDER, LOUDER CUT -- the repair this sheet exists to test. The shipped
     woosh sweeps 360 -> 1190 Hz; the B1 bed sits at 380-1020. They occupy THE
     SAME BAND, and filtered noise over filtered noise is camouflage rather
     than a layer -- which is how a sound can be present, measurable and still
     inaudible. This one starts lower and ends far higher, so it crosses OUT
     of the bed at both ends, where there is nothing to hide it. */
  const wooshWide = (t, n) => {
    const base = 210 + (n % 3) * 60;
    [[0.00,1.00,0.070],[0.06,2.60,0.095],[0.13,5.20,0.090],
     [0.21,8.40,0.075],[0.30,4.60,0.050],[0.40,2.00,0.030]].forEach(([d,k,g]) =>
      B(t + d, { freq: base * k, q: 0.62, gain: g, dur: 0.28,
                 type:"bandpass" }));
    B(t + 0.08, { freq: 140, q: 0.5, gain: 0.042, dur: 0.46, type:"lowpass" });
  };

  /* THE B1 BED, verbatim -- the thing it has to be heard over. */
  const bed = (t, n) => {
    const w = 640 + Math.sin(n * 0.37) * 260 + Math.sin(n * 0.11) * 120;
    B(t, { freq: w, q: 0.42, gain: 0.085, dur: 0.42, type:"bandpass" });
    B(t, { freq: 190, q: 0.5, gain: 0.045, dur: 0.40, type:"lowpass" });
    if (n % 5 === 0)
      B(t + 0.05, { freq: 2600, q: 1.5, gain: 0.020, dur: 0.05,
                    type:"bandpass" });
  };
  const runBed = (t0, dur) => {
    for (let n = 0; n * 0.26 < dur; n++) bed(t0 + n * 0.26, n);
  };

  const marks = [];
  let t = 1.0;
  const sec = (label, f, adv) => {
    marks.push({ label: label, t: +t.toFixed(2) }); f(t); t += adv;
  };

  sec("W1 the OLD one (ticks)", (t0) => {
    for (let n = 0; n < 3; n++) woosh(t0 + n * 1.15, n); }, 4.4);
  sec("W3 swept, alone", (t0) => {
    for (let n = 0; n < 3; n++) wooshSwept(t0 + n * 1.15, n); }, 4.4);
  sec("W3 over the bed", (t0) => {
    runBed(t0, 3.6);
    for (let n = 0; n < 3; n++) wooshSwept(t0 + 0.3 + n * 1.15, n); }, 4.8);
  sec("W4 slower, alone", (t0) => {
    for (let n = 0; n < 3; n++) wooshSlow(t0 + n * 1.30, n); }, 4.6);
  sec("W4 over the bed", (t0) => {
    runBed(t0, 3.8);
    for (let n = 0; n < 3; n++) wooshSlow(t0 + 0.3 + n * 1.30, n); }, 4.8);

  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){
    out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v;
  }
  const secPeak = marks.map((m, i) => {
    const a = Math.round(m.t * sr);
    const b = Math.round((i + 1 < marks.length ? marks[i+1].t : secs) * sr);
    let pk = 0, sum = 0, n2 = 0;
    for (let k = a; k < b && k < d.length; k++){
      const v = Math.abs(d[k]); if (v > pk) pk = v; sum += v * v; n2++;
    }
    return { label: m.label, t: m.t, peak: +pk.toFixed(4),
             rms: +Math.sqrt(sum / Math.max(1, n2)).toFixed(4) };
  });
  return { pcm: out, sr, peak: +peak.toFixed(3), marks: secPeak };
}"""


RENDER_JS = r"""async ([gap, secs, hold, rate]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv = {on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise};
  const oc = new OC(1, Math.round(sr * secs), sr);
  S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = S._noiseBuffer();
  const B = (t, o) => S._burst(t, o);
  const T = (t, o) => S._tone(t, o);

  /* ---- THE THREE CASTS ---- */
  const CAST = [];
  /* A1 UPDRAFT -- air pulled off the floor. The sweep is in the FILTER, not in
     a tone: a rising pitch is a whistle and a rising cutoff is wind. Six
     overlapping bursts because one 0.9s burst would play silence for its tail
     (4.5). */
  CAST.push((t) => {
    [[0,300,0.10],[0.10,520,0.13],[0.20,820,0.15],
     [0.30,1250,0.15],[0.40,1800,0.13],[0.50,2500,0.10]]
      .forEach(([d,f,g]) =>
        B(t + d, { freq: f, q: 0.55, gain: g, dur: 0.34, type:"bandpass" }));
    T(t + 0.44, { freq: 150, to: 46, gain: 0.34, dur: 0.85, type:"sine" });
    B(t + 0.46, { freq: 220, q: 0.5, gain: 0.26, dur: 0.70, type:"lowpass" });
  });
  /* A2 RIFT -- the hall tearing. Crack first, then the pair falls away, so the
     loudest moment is the FIRST one and the window opens under it. */
  CAST.push((t) => {
    B(t, { freq: 5200, q: 0.9, gain: 0.30, dur: 0.09, type:"highpass" });
    B(t + 0.01, { freq: 700, q: 0.6, gain: 0.32, dur: 0.34, type:"bandpass" });
    T(t + 0.02, { freq: 320, to: 62, gain: 0.30, dur: 0.75, type:"sawtooth" });
    T(t + 0.06, { freq: 214, to: 48, gain: 0.18, dur: 0.80, type:"sawtooth" });
    B(t + 0.30, { freq: 180, q: 0.5, gain: 0.20, dur: 0.55, type:"lowpass" });
  });
  /* A3 INHALE -- a swell, a snap, a drop. The only one whose loudest point is
     LATE, which is what makes it read as something starting rather than
     something landing. */
  CAST.push((t) => {
    [[0,0.05],[0.12,0.08],[0.24,0.12],[0.36,0.17]].forEach(([d,g]) =>
      B(t + d, { freq: 900, q: 0.7, gain: g, dur: 0.30, type:"bandpass" }));
    B(t + 0.50, { freq: 3000, q: 1.3, gain: 0.26, dur: 0.07, type:"bandpass" });
    T(t + 0.52, { freq: 420, to: 54, gain: 0.32, dur: 0.90, type:"triangle" });
    B(t + 0.54, { freq: 160, q: 0.5, gain: 0.24, dur: 0.80, type:"lowpass" });
  });

  /* ---- THE THREE HOLDS. Each is ONE STRIKE; the driver below re-strikes it
     at the candidate's own cadence, because a held note does not exist here. */
  const HOLD = [
    { cad: 0.26, f: (t, n) => {                       // B1 WIND
        const w = 640 + Math.sin(n * 0.37) * 260 + Math.sin(n * 0.11) * 120;
        B(t, { freq: w, q: 0.42, gain: 0.085, dur: 0.42, type:"bandpass" });
        B(t, { freq: 190, q: 0.5, gain: 0.045, dur: 0.40, type:"lowpass" });
        if (n % 5 === 0)
          B(t + 0.05, { freq: 2600, q: 1.5, gain: 0.020, dur: 0.05,
                        type:"bandpass" });
      } },
    { cad: 0.16, f: (t, n) => {                       // B2 TURBINE
        const w = 1 + Math.sin(n * 0.9) * 0.014;
        T(t, { freq: 62 * w, to: 58 * w, gain: 0.090, dur: 0.34,
               type:"sawtooth" });
        T(t, { freq: 93 * w, to: 87 * w, gain: 0.042, dur: 0.30,
               type:"sawtooth" });
        B(t, { freq: 1400, q: 0.5, gain: 0.022, dur: 0.20, type:"bandpass" });
      } },
    { cad: 0.44, f: (t, n) => {                       // B3 HOLLOW
        const w = 1 + ((n * 29) % 5 - 2) * 0.005;
        T(t, { freq: 74 * w, to: 70 * w, gain: 0.105, dur: 0.72, type:"sine" });
        T(t, { freq: 222 * w, to: 214 * w, gain: 0.026, dur: 0.55,
               type:"triangle" });
        if (n % 2 === 0)
          B(t, { freq: 520, q: 0.9, gain: 0.028, dur: 0.34, type:"bandpass" });
      } },
  ];

  /* ---- THE TWO TICKS, at the REAL RATE. This is the only question that
     cannot be asked with one strike: 7 a second is 143ms apart, and whether
     that is a grind or a buzz is a property of the SPACING as much as of the
     sound. */
  const TICK = [
    (t, n) => {                                       // C1 ZAP
      B(t, { freq: 3200, q: 1.7, gain: 0.075, dur: 0.030, type:"bandpass" });
      B(t, { freq: 900,  q: 1.1, gain: 0.030, dur: 0.026, type:"bandpass" });
    },
    (t, n) => {                                       // C2 BITE
      B(t, { freq: 2400, q: 1.4, gain: 0.055, dur: 0.022, type:"bandpass" });
      T(t, { freq: 1180 + (n % 3) * 90, to: 640, gain: 0.045, dur: 0.075,
             type:"triangle" });
    },
  ];

  const marks = [];
  let t = 1.0;   /* SFX schedules from currentTime = 1.0 (v59: a 1.0s window
                    renders NOTHING), so the sheet starts there. */

  const runHold = (t0, dur, hi, ti) => {
    const H = HOLD[hi];
    for (let n = 0; n * H.cad < dur; n++) H.f(t0 + n * H.cad, n);
    if (ti >= 0)
      for (let n = 0; n / rate < dur; n++) TICK[ti](t0 + n / rate, n);
  };

  /* A -- the three casts, each dropping into 1.6s of a NEUTRAL hold (B1), so
     each is heard ARRIVING into a window rather than in silence. */
  for (let i = 0; i < 3; i++){
    marks.push({ label: "A" + (i+1), t: +(t).toFixed(2) });
    CAST[i](t);
    runHold(t + 0.65, 1.6, 0, -1);
    t += gap;
  }
  /* B -- the three holds, each `hold` seconds long with the NEUTRAL tick (C1)
     over the top at the real rate, opened by the neutral cast (A1). The
     question is whether ten seconds of it wears out and whether the ticks
     still cut through. */
  for (let i = 0; i < 3; i++){
    marks.push({ label: "B" + (i+1), t: +(t).toFixed(2) });
    CAST[0](t);
    runHold(t + 0.65, hold, i, 0);
    t += hold + 1.6;
  }
  /* C -- the two ticks, at SEVEN A SECOND over the neutral hold. */
  for (let i = 0; i < 2; i++){
    marks.push({ label: "C" + (i+1), t: +(t).toFixed(2) });
    runHold(t, 3.2, 0, i);
    t += 4.4;
  }

  const buf = await oc.startRendering();
  S.on=sv.on; S.ok=sv.ok; S.ctx=sv.ctx; S.bus=sv.bus; S.noise=sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  let peak = 0;
  for (let i = 0; i < d.length; i++){
    out[i] = d[i];
    const v = Math.abs(d[i]); if (v > peak) peak = v;
  }
  /* PER-SECTION PEAKS, because "it rendered" and "it made a sound" are
     different claims and v42 shipped a SILENT ultimate through every check in
     this repo. A section at peak 0.000 is a candidate that does not exist. */
  const secPeak = marks.map((m, i) => {
    /* THE HOLD SECTIONS SKIP THEIR OWN CAST. Each B section opens with the
       neutral cast so the hold is heard being arrived at -- and the cast is
       far louder than any hold, so a naive section peak reports the CAST's
       number under the HOLD's name. B1 and B3 both came back at exactly
       A1's 0.434 before this, which is the tell: two different candidates
       cannot have identical peaks to three decimals. */
    const skip = m.label[0] === "B" ? 1.9 : 0.0;
    const a = Math.round((m.t + skip) * sr);
    const b = Math.round((i + 1 < marks.length ? marks[i+1].t : secs) * sr);
    let p = 0;
    for (let k = a; k < b && k < d.length; k++){
      const v = Math.abs(d[k]); if (v > p) p = v;
    }
    return { label: m.label, t: m.t, peak: +p.toFixed(4) };
  });
  return { pcm: out, sr, peak: +peak.toFixed(3), marks: secPeak };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vortex.html")
    ap.add_argument("--gap", type=float, default=3.2)
    ap.add_argument("--hold", type=float, default=6.0,
                    help="seconds of standing tornado per hold candidate "
                         "(the real window is 10)")
    ap.add_argument("--rate", type=float, default=7.0,
                    help="ticks a second -- the relic's own, and the whole "
                         "question for section C")
    ap.add_argument("--out", default="../05-reference/v63/scour-voices.wav")
    ap.add_argument("--woosh", action="store_true",
                    help="the woosh ALONE, then against the bed, then a "
                         "wider cut. Rick could not hear it in the clip.")
    A = ap.parse_args()
    if A.woosh and A.out.endswith("scour-voices.wav"):
        A.out = "../05-reference/v63/scour-woosh-alone.wav"

    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    secs = 1.0 + A.gap * 3 + (A.hold + 1.6) * 3 + 4.4 * 2 + 2.0

    if A.woosh:
        secs = 1.0 + 4.4 + 4.4 + 4.8 + 4.4 + 4.8 + 1.0
    with game(game_path=resolve_game(A.game)) as (page, errors):
        if A.woosh:
            r = page.evaluate(WOOSH_JS, [secs])
        else:
            r = page.evaluate(RENDER_JS, [A.gap, secs, A.hold, A.rate])
        assert not errors, errors[:3]

    import numpy as np
    d = np.asarray(r["pcm"], dtype=np.float32)
    pcm = np.clip(d * 0.92 / max(1e-9, np.abs(d).max()), -1, 1)
    w = wave.open(str(out), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(r["sr"])
    w.writeframes((pcm * 32767).astype("<i2").tobytes())
    w.close()

    if A.woosh:
        print("")
        print("THE WOOSH, ALONE AND AGAINST THE BED   (%.0fs)" % secs)
        print("")
        for mk in r["marks"]:
            print("    %5.1fs  %-24s peak %.4f  rms %.4f"
                  % (mk["t"], mk["label"], mk["peak"], mk["rms"]))
        print("")
        print("  WHAT THIS SHEET TESTS. `_burst` sets its filter with")
        print("  setValueAtTime -- FIXED, never ramped -- and its gain starts")
        print("  at full and decays. That is a percussive envelope on a static")
        print("  filter, so EVERY `_burst` IS A TICK BY CONSTRUCTION, and five")
        print("  at rising frequencies is a xylophone run. Rick: \"those read")
        print("  as ticks not wooshes.\" W1 above is that, kept as the control.")
        print("")
        print("  W3 and W4 use `_sweep`, a new primitive: the filter RAMPS")
        print("  across the duration so the band moves, and the gain has an")
        print("  ATTACK so there is no transient to hear as a tick. Up then")
        print("  down, because something passing gets closer and then goes")
        print("  away -- a sweep that only rises is a siren.")
        print("")
        print("  wrote %s" % out)
        return 0

    print(f"\nSCOUR -- THE VOICE, AS A SPREAD   ({secs:.0f}s, raw peak "
          f"{r['peak']})\n")
    print("  A. THE CAST -- each drops into 1.6s of a neutral hold")
    for (name, what), m in zip(CASTS, r["marks"][:3]):
        print(f"    {m['t']:5.1f}s  {name:14} peak {m['peak']:.3f}   {what}")
    print(f"\n  B. THE HOLD -- {A.hold:g}s each, neutral cast in, neutral tick "
          f"over the top at {A.rate:g}/s")
    for (name, what), m in zip(HOLDS, r["marks"][3:6]):
        print(f"    {m['t']:5.1f}s  {name:14} peak {m['peak']:.3f}   {what}")
    print(f"\n  C. THE TICK -- {A.rate:g} A SECOND over a neutral hold. The "
          f"question is\n     whether that is a grind or a buzz.")
    for (name, what), m in zip(TICKS, r["marks"][6:8]):
        print(f"    {m['t']:5.1f}s  {name:14} peak {m['peak']:.3f}   {what}")

    dead = [m["label"] for m in r["marks"] if m["peak"] < 0.005]
    if dead:
        print(f"\n  SILENT SECTIONS: {dead} -- a candidate that renders at "
              f"peak 0 does not\n  exist, and v42 shipped exactly that through "
              f"every check in this repo.")
    else:
        print("\n  every section rendered audibly (peak >= 0.005). That is "
              "asserted, not\n  assumed -- `SFX.play` returns on its first "
              "line headless and wraps its\n  body in try/catch, so a broken "
              "voice is invisible to every other tool.")
    print(f"\n  wrote {out}")
    print("\n  NOTHING IS WIRED IN. Scour currently falls through the `ult`")
    print("  dispatch to the RUNE-CRACK -- runic's half-second burst -- and")
    print("  then makes no sound for the rest of its ten-second window. The")
    print("  chosen voice goes into `duskreave_build.py` by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
