"""The first sample (left channel, 16-bit) where two renders differ by MORE than 1 LSB -- a pinned render's own
floor is 1 LSB (float summation order in the audio graph) -- and the largest difference before it.
    python first_real_diff.py <dir> <a.wav> <b.wav> [<a.wav> <b.wav> ...]"""
import sys, wave, numpy as np
D = sys.argv[1]
def L(p):
    w = wave.open(f"{D}/{p}"); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(int).reshape(-1, w.getnchannels())[:, 0]
for a, b in zip(sys.argv[2::2], sys.argv[3::2]):
    d = np.abs(L(a) - L(b)); i = np.nonzero(d > 1)[0]
    if not len(i):
        print(f"{a} vs {b}: never more than 1 LSB apart (max {d.max()} LSB)"); continue
    print(f"{a} vs {b}: at most {d[:i[0]].max()} LSB apart until {i[0] / 48000:.4f} s video (match {77.98333 + i[0] / 48000:.4f}); "
          f"the cast is recorded at wall 1.1833 (match 79.1667)")
