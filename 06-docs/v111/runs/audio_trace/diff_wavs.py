"""Level of the DIFFERENCE between two wavs, against the level of the mix, in windows over time.

    python diff_wavs.py <a.wav> <b.wav> [--win 0.5] [--t0 77.98333] [--label text]

Reads 16-bit PCM (mono or stereo; stereo is read as L and R separately and reported per channel pair
as the mean). Prints, per window: rms(a) dBFS, rms(a-b) dBFS, and (a-b) relative to a in dB; then the
whole-track figures, the first sample that differs, the max abs sample difference, and the band split of
the difference (so "broadband" can be checked rather than asserted).
"""
import sys, wave, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("a"); ap.add_argument("b")
ap.add_argument("--win", type=float, default=0.5)
ap.add_argument("--t0", type=float, default=77.98333, help="match time of the first sample")
ap.add_argument("--label", default="")
ap.add_argument("--quiet", action="store_true", help="whole-track lines only")
a = ap.parse_args()


def load(p):
    w = wave.open(p)
    ch, sr, n = w.getnchannels(), w.getframerate(), w.getnframes()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return x.reshape(-1, ch), sr


x, sr = load(a.a); y, sr2 = load(a.b)
assert sr == sr2, (sr, sr2)
n = min(len(x), len(y)); x, y = x[:n], y[:n]
d = x - y
db = lambda v: 20 * np.log10(v + 1e-12)
rms = lambda v: np.sqrt(np.mean(v ** 2))

print(f"{a.label}  A={a.a}  B={a.b}")
print(f"  {n} frames x {x.shape[1]} ch at {sr} Hz ({n / sr:.3f} s); len A {len(x)} B {len(y)}")
nz = np.nonzero(np.any(d != 0, axis=1))[0]
if len(nz) == 0:
    print("  BIT-IDENTICAL over the common length")
    sys.exit(0)
print(f"  samples that differ: {len(nz)} of {n} ({100 * len(nz) / n:.1f}%); first at {nz[0] / sr:.4f} s "
      f"(match {a.t0 + nz[0] / sr:.3f}); max |A-B| {np.abs(d).max():.5f} ({db(np.abs(d).max()):.1f} dBFS)")
print(f"  whole track: rms A {db(rms(x)):.1f} dBFS, rms B {db(rms(y)):.1f}, rms(A-B) {db(rms(d)):.1f} dBFS "
      f"= {db(rms(d)) - db(rms(x)):+.1f} dB re A")
# band split of the difference (whole track, first channel)
D = np.abs(np.fft.rfft(d[:, 0])) ** 2; fr = np.fft.rfftfreq(n, 1 / sr)
X = np.abs(np.fft.rfft(x[:, 0])) ** 2
print("  band        diff dB re A's own band   (share of the difference's power)")
tot = D.sum()
for f0, f1 in [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000), (8000, 24000)]:
    m = (fr >= f0) & (fr < f1)
    print(f"    {f0:>5}-{f1:<5} Hz  {10 * np.log10(D[m].sum() / (X[m].sum() + 1e-30) + 1e-30):+6.1f} dB"
          f"   ({100 * D[m].sum() / tot:5.1f}%)")
if a.quiet:
    sys.exit(0)
print(f"  window {a.win}s:   video    match     rms A   rms(A-B)   re A")
w = int(a.win * sr)
for i in range(0, n - w + 1, w):
    xa, da = x[i:i + w], d[i:i + w]
    print(f"            {i / sr:7.2f}  {a.t0 + i / sr:7.2f}   {db(rms(xa)):6.1f}   {db(rms(da)):7.1f}   {db(rms(da)) - db(rms(xa)):+6.1f}")
