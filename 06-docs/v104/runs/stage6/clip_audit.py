"""v104 stage 6, scratch: ARE ASCENSION'S VOICES IN THE CLIP'S AUDIO? (v106's drip_audit.py, for four voices.)

The clip's wav (48 kHz) in 10 ms hops of a 4096-point Hann FFT. Each voice is looked for where the voice lab put
it, as the onsets of a narrow band against a reference band where it does not sound:
  - the cast chord: D4 294 / A4 440 / D5 587 Hz (+-6), all three together, against 360-400 Hz;
  - the taps: C8-A8 (4150-7100 Hz) against 2300-3800 Hz (the wall tick's 3 kHz lives there, so a wall tick
    does not count as a tap);
  - the close: A3 220 / E4 330 Hz (+-6) together, against 250-300 Hz;
  - the thud: 40-100 Hz against 150-240 Hz.
An onset is a hop whose band rises 8 dB over its own running median of the previous 300 ms and stands 6 dB over
its reference band; onsets closer than 60 ms (taps) or 400 ms (the others) are one.

    python clip_audit.py <clip.wav>
"""
import sys, wave, numpy as np

p = sys.argv[1]
w = wave.open(p); sr = w.getframerate(); ch = w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
if ch > 1:
    x = x.reshape(-1, ch).mean(1)
N, H = 4096, sr // 100
win = np.hanning(N); f = np.fft.rfftfreq(N, 1 / sr)
frames = np.array([x[i:i + N] * win for i in range(0, len(x) - N, H)])
S = np.abs(np.fft.rfft(frames, axis=1)) ** 2
t = (np.arange(len(frames)) * H + N / 2) / sr


def band(lo, hi):
    return 10 * np.log10(S[:, (f >= lo) & (f <= hi)].mean(1) + 1e-20)


def onsets(b, ref, gap, rise=8.0, over=6.0):
    on = []
    for i in range(30, len(b)):
        med = np.median(b[i - 30:i])
        if b[i] - med > rise and b[i] - ref[i] > over and (not on or t[i] - on[-1] > gap):
            on.append(round(float(t[i]), 2))
    return on


def tones(fs, ref, gap):
    bs = [band(c - 6, c + 6) for c in fs]
    b = np.min(np.array(bs), axis=0)          # all the tones together: the weakest of them
    return onsets(b, ref, gap)


print(f"CLIP AUDIT {p.replace(chr(92), '/').split('/')[-1]}  {len(x) / sr:.2f}s, {sr} Hz")
print(f"  cast chord (D4 A4 D5 together):  onsets at {tones([293.7, 440.0, 587.3], band(360, 400), 0.4)}")
print(f"  taps (C8-A8, 4150-7100 Hz):      onsets at {onsets(band(4150, 7100), band(2300, 3800), 0.06)}")
print(f"  close (A3 E4 together):          onsets at {tones([220.0, 329.6], band(250, 300), 0.4)}")
print(f"  thud (40-100 Hz):                onsets at {onsets(band(40, 100), band(150, 240), 0.4)}")
