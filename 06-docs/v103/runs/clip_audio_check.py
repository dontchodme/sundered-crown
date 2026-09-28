"""The clip's voices, read off its AAC (decoded to mono 48k by ffmpeg: clip_audio.wav). Clip time =
match time - 30.858 (the clip's first frame). Events from clip_timeline.txt."""
import sys, wave, struct, math
w = wave.open(sys.argv[1]); n = w.getnframes(); sr = w.getframerate()
x = [v / 32768 for v in struct.unpack("<%dh" % n, w.readframes(n))]
db = lambda v: 20 * math.log10(v + 1e-12)
def g(f, a, b):
    s = x[int(a * sr):int(b * sr)]; k = 2 * math.cos(2 * math.pi * f / sr); p = q = 0.0
    for v in s: p, q = v + k * p - q, p
    return math.sqrt(max(0.0, p * p + q * q - k * p * q)) / len(s)
print("CAST at 1.20: the ring's partials, 1.28-1.78 against 0.60-1.10 (before the cast)")
for f in (110, 303.6, 594, 982.3):
    print(f"  {f:6.1f} Hz  {db(g(f, 1.28, 1.78)) - db(g(f, 0.6, 1.1)):+5.1f} dB")
print("ANVILS: the note for the loser's count (A5 x 2^((n-1)/12)), 100 ms from the bind against the 100 ms before")
for n_, t in ((2, 1.950), (4, 3.267), (6, 4.083), (8, 6.142), (9, 7.833), (9, 9.908)):
    f = 880 * 2 ** ((n_ - 1) / 12)
    print(f"  n{n_} {f:7.1f} Hz at {t:6.3f}s: {db(g(f, t, t + 0.1)) - db(g(f, t - 0.1, t)):+5.1f} dB")
print("CLOSE at 11.075 (clock): its 303.6 Hz mode against its neighbours (260 / 350 Hz), 250 ms spans")
for a in (10.30, 10.55, 10.80, 11.05, 11.30, 11.55, 11.80):
    c = g(303.6, a, a + 0.25); nb = (g(260, a, a + 0.25) + g(350, a, a + 0.25)) / 2
    print(f"  {a:5.2f}-{a+0.25:5.2f}s  303.6 Hz {db(c):6.1f} dBFS   neighbours {db(nb):6.1f}   tone over neighbours {db(c)-db(nb):+5.1f} dB")
