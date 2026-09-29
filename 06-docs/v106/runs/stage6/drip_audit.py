"""Scratch: are the drips in the clip's audio? Narrow bands where the reversed drip lands (count 2: 1081 Hz,
count 4: 1358 Hz; the voice lab's measured landings), against a reference band between them (1215 +- 25 Hz,
where no count lands) and against the stretch before the cast. Onsets: 10 ms frames whose landing-band level
rises 8 dB over the band's running median of the previous 300 ms and stands 6 dB over the reference band."""
import sys, wave, numpy as np
p = sys.argv[1]; t_cast, t_close = float(sys.argv[2]), float(sys.argv[3])
w = wave.open(p); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
N, H = 4096, 480
win = np.hanning(N); f = np.fft.rfftfreq(N, 1 / sr)
def band(S, lo, hi): return 10 * np.log10(S[:, (f >= lo) & (f <= hi)].mean(1) + 1e-20)
frames = np.array([x[i:i + N] * win for i in range(0, len(x) - N, H)])
S = np.abs(np.fft.rfft(frames, axis=1)) ** 2
t = (np.arange(len(frames)) * H + N / 2) / sr
out = []
for name, c in (("count 4, E6 1358 Hz", 1358), ("count 2, C6 1081 Hz", 1081)):
    b = band(S, c - 25, c + 25); ref = band(S, 1190, 1240)
    on = []
    for i in range(30, len(b)):
        med = np.median(b[i - 30:i])
        if b[i] - med > 8 and b[i] - ref[i] > 6 and (not on or t[i] - on[-1] > 0.06): on.append(t[i])
    on = np.array(on)
    pre = on[on < t_cast]; inw = on[(on >= t_cast) & (on <= t_close)]; post = on[on > t_close + 0.2]
    out.append(f"  {name}: onsets before the cast {len(pre)} ({len(pre) / max(t_cast, 1e-9):.2f}/s), in the window {len(inw)} "
               f"({len(inw) / (t_close - t_cast):.2f}/s), after the close {len(post)}")
print(f"DRIP AUDIT {p.split('/')[-1]}  cast at {t_cast}s, close at {t_close}s of video")
print("\n".join(out))
