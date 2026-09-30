"""rms(A-B) in dBFS per window, several pairs side by side (mono: channels averaged), over the clip's 12.77 s; plus
each pair's first differing sample. The window rows are marked with what the fx link adds in them (cast 79.167,
stun voices, close 88.933, from events_diff.py) so the no-new-voice rows can be read on their own.
    python window_table.py <win> <label> <a.wav> <b.wav> [<label> <a.wav> <b.wav> ...]"""
import sys, wave
import numpy as np
T0, DUR = 77.98333, 12.767
NEW = [1.1833, 1.3, 1.6, 1.8833, 2.3333, 4.05, 4.6167, 5.2667, 5.6333, 6.1, 6.3333, 6.5667, 6.8833, 7.2, 7.5167, 7.8333,
       8.0667, 8.3, 8.5333, 8.7667, 9.25, 9.4833, 9.7167, 9.95, 10.2667, 10.5, 10.7333, 10.95]   # wall s, fx only / redesigned


def load(p):
    w = wave.open(p); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x.reshape(-1, ch).mean(axis=1), w.getframerate()


win = float(sys.argv[1]); args = sys.argv[2:]
pairs = []
for i in range(0, len(args), 3):
    lab, pa, pb = args[i:i + 3]
    x, sr = load(pa); y, _ = load(pb); n = min(len(x), len(y), int(DUR * sr))
    d = x[:n] - y[:n]; nz = np.nonzero(d)[0]
    pairs.append((lab, d, sr, x[:n]))
    print(f"  {lab:40s} first differing sample at {nz[0] / sr if len(nz) else float('nan'):.4f} s video")
print(f"{'video':>6} {'match':>6}  new voice sounding?  " + "".join(f"{p[0][:22]:>24s}" for p in pairs))
db = lambda v: 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-12)
w0 = 0.0
while w0 + win <= DUR + 1e-9:
    busy = any(w0 - 0.45 < t < w0 + win for t in NEW)   # a new voice started in the window or <0.45 s before it
    row = f"{w0:6.2f} {T0 + w0:6.2f}  {'yes' if busy else ' - ':^19s}  "
    for lab, d, sr, x in pairs:
        a, b = int(w0 * sr), int((w0 + win) * sr)
        row += f"{db(d[a:b]):16.1f} ({db(d[a:b]) - db(x[a:b]):+5.1f})"
    print(row); w0 += win
print("each cell: rms(A-B) dBFS (and re rms A)")
