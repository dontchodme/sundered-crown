"""The clip's voices, read off its AAC (decoded to mono 48k by ffmpeg: clip_audio.wav). Clip time = match
time - T0 (the clip's first frame, from clip.log). Events from clip_timeline.json.
  usage: clip_audio_check.py clip_audio.wav T0"""
import sys, wave, struct, math, json, pathlib
S = pathlib.Path(__file__).resolve().parent
w = wave.open(sys.argv[1]); n = w.getnframes(); sr = w.getframerate(); T0 = float(sys.argv[2])
x = [v / 32768 for v in struct.unpack("<%dh" % n, w.readframes(n))]
db = lambda v: 20 * math.log10(v + 1e-12)
def g(f, a, b):
    """Goertzel magnitude of f over [a, b) seconds of the clip."""
    a, b = max(0, a), max(0, b)
    s = x[int(a * sr):int(b * sr)]
    if not s: return 0.0
    k = 2 * math.cos(2 * math.pi * f / sr); p = q = 0.0
    for v in s: p, q = v + k * p - q, p
    return math.sqrt(max(0.0, p * p + q * q - k * p * q)) / len(s)
def rms(a, b):
    s = x[int(max(0, a) * sr):int(max(0, b) * sr)]
    return math.sqrt(sum(v * v for v in s) / max(1, len(s)))
ev = json.load(open(S / "clip_timeline.json"))
cast = [e for e in ev if e[0] == "cast"][0][1] - T0
print(f"CLIP {sys.argv[1]}  {n / sr:.2f}s  first frame at match {T0:.3f}")
print(f"CAST at clip {cast:.3f}: the bellows' band (150-300 Hz: 200 / 250 Hz), 0.10-0.50 s after the cast against the 0.4 s before")
for f in (200, 250):
    print(f"  {f:4d} Hz  {db(g(f, cast + 0.10, cast + 0.50)) - db(g(f, cast - 0.45, cast - 0.05)):+5.1f} dB")
print("LANDINGS: the body note for the foe's count (110 x 2^((n-1)/12)) and its iron partial (x 2.76, where a phone hears it),")
print("          the 60 ms from the landing against the 60 ms before")
for e in ev:
    if e[0] != "landing": continue
    t, k = e[1] - T0, e[2]; kk = min(max(k, 1), 6); f = 110 * 2 ** ((kk - 1) / 12)
    print(f"  n{k} at {t:6.3f}s  body {f:6.1f} Hz {db(g(f, t, t + 0.06)) - db(g(f, t - 0.06, t)):+5.1f} dB   "
          f"iron {f * 2.76:6.1f} Hz {db(g(f * 2.76, t, t + 0.06)) - db(g(f * 2.76, t - 0.06, t)):+5.1f} dB")
print("MISSES: the miss's note (103.83 Hz) and its iron (286.6 Hz), 60 ms from the miss against the 60 ms before")
for e in ev:
    if e[0] != "miss": continue
    t = e[1] - T0
    print(f"  miss at {t:6.3f}s  103.8 Hz {db(g(103.83, t, t + 0.06)) - db(g(103.83, t - 0.06, t)):+5.1f} dB   "
          f"286.6 Hz {db(g(286.6, t, t + 0.06)) - db(g(286.6, t - 0.06, t)):+5.1f} dB")
cl = [e for e in ev if e[0] == "close"]
if cl:
    t = cl[0][1] - T0
    print(f"CLOSE at clip {t:.3f} ({cl[0][3]}): the design gives it no voice -- the level around it (dBFS, 100 ms spans)")
    for a in (t - 0.3, t - 0.2, t - 0.1, t, t + 0.1, t + 0.2, t + 0.3):
        print(f"  {a:6.2f}-{a + 0.1:6.2f}s  {db(rms(a, a + 0.1)):6.1f} dBFS   bellows band 200 Hz {db(g(200, a, a + 0.1)):6.1f}")
