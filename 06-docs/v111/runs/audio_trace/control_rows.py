"""clip_audio6.py's CONTROL rows (the same bands, times and windows, the same Hann-windowed FFT band power) read on
pairs of renderAudio's own PCM instead of the AAC decodes: a pair whose difference is the render and not the build
must reproduce the integrator's no-voice spread if the spread is the render's.
    python control_rows.py <label> <a.wav> <b.wav> [<label> <a.wav> <b.wav> ...]"""
import sys, wave
import numpy as np
T0 = 77.98333
CT = [("C4 band, before the cast", t, 0.0, 0.28, 252, 272) for t in (78.10, 78.55)]
CT += [("C4 band, after the close's hum", t, 0.0, 0.28, 252, 272) for t in (89.45, 89.90, 90.30)]
CT += [("sizzle band, before the cast", t, 0.06, 0.30, 2400, 2800) for t in (78.10, 78.55)]
CT += [("sizzle band, after the last stun", t, 0.06, 0.30, 2400, 2800) for t in (89.45, 89.90, 90.30)]


def load(p):
    w = wave.open(p); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x.reshape(-1, ch).mean(axis=1), w.getframerate()


def band(sig, sr, t0, t1, f0, f1):
    a, b = int(t0 * sr), int(t1 * sr)
    seg = sig[a:b] * np.hanning(b - a)
    sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(b - a, 1 / sr)
    return 10 * np.log10(sp[(fr >= f0) & (fr < f1)].sum() + 1e-12)


args = sys.argv[1:]
print(f"{'':34s}" + "".join(f"{r[0][:6] + ' ' + str(r[1]):>13s}" for r in CT) + "   max|d| C4 / sizzle")
for i in range(0, len(args), 3):
    lab, pa, pb = args[i:i + 3]
    x, sr = load(pa); y, _ = load(pb); n = min(len(x), len(y)); x, y = x[:n], y[:n]
    ds = [band(x, sr, t - T0 + a, t - T0 + b, f0, f1) - band(y, sr, t - T0 + a, t - T0 + b, f0, f1)
          for (_, t, a, b, f0, f1) in CT]
    print(f"{lab:34s}" + "".join(f"{d:+13.1f}" for d in ds)
          + f"   {max(abs(d) for d in ds[:5]):.1f} / {max(abs(d) for d in ds[5:]):.1f}")
