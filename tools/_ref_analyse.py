"""MEASURE A REFERENCE SOUND SO A SYNTHESISED ONE CAN BE MATCHED TO IT.

Rick supplied a reference for the nova and said to ignore the last second. This
project has no sampler -- every voice is synthesised in WebAudio -- so a
reference cannot be used, only MEASURED and matched. The vocabulary is v54's,
which is how Deadfall's explosion was resized: peak, audible duration, and the
share of energy below 120 Hz.
"""
import argparse, math, sys, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--upto", type=float, default=3.0)
a = ap.parse_args()

w = wave.open(a.path, "rb")
sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
raw = w.readframes(n)
dt = {1: np.int8, 2: np.int16, 4: np.int32}[sw]
x = np.frombuffer(raw, dtype=dt).astype(np.float64)
if ch > 1: x = x.reshape(-1, ch).mean(axis=1)
x /= (np.abs(x).max() or 1)
print(f"\n  {a.path.split(chr(92))[-1]}")
print(f"  {sr} Hz, {ch}ch, {sw*8}-bit, {n/sr:.2f}s total; reading first {a.upto:.1f}s\n")
x = x[:int(a.upto * sr)]

env = np.abs(x)
k = max(1, int(0.005 * sr))
env = np.convolve(env, np.ones(k)/k, mode="same")
pk = env.max(); pi = int(env.argmax())
print(f"  PEAK              {pk:.3f} at {pi/sr*1000:.0f} ms")
for thr in (0.5, 0.1, 0.02):
    idx = np.where(env > pk*thr)[0]
    if len(idx): print(f"  above {thr:>4.0%} of peak   {idx[-1]/sr:.2f}s  "
                       f"(from {idx[0]/sr*1000:.0f} ms)")

def band(seg):
    if len(seg) < 64: return None
    win = seg * np.hanning(len(seg))
    S = np.abs(np.fft.rfft(win))**2
    f = np.fft.rfftfreq(len(seg), 1/sr)
    tot = S.sum() or 1
    cen = float((f*S).sum()/tot)
    return (cen, S[f < 120].sum()/tot, S[(f>=120)&(f<500)].sum()/tot,
            S[(f>=500)&(f<2000)].sum()/tot, S[f>=2000].sum()/tot)

print(f"\n  SPECTRUM OVER TIME (energy share)\n")
print(f"    {'window':>12}{'centroid':>10}{'<120Hz':>9}{'120-500':>9}"
      f"{'500-2k':>9}{'>2k':>8}")
for lo, hi in [(0,.05),(.05,.15),(.15,.4),(.4,.8),(.8,1.6),(1.6,3.0)]:
    seg = x[int(lo*sr):int(hi*sr)]
    b = band(seg)
    if not b: continue
    print(f"    {lo:.2f}-{hi:.2f}s{b[0]:>10.0f}{b[1]:>9.1%}{b[2]:>9.1%}"
          f"{b[3]:>9.1%}{b[4]:>8.1%}")
b = band(x)
print(f"\n  WHOLE CLIP        centroid {b[0]:.0f} Hz   <120Hz {b[1]:.1%}")
