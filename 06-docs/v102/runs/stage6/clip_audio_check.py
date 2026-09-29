"""The clip's voices, read off its AAC (decoded to mono 48k by ffmpeg: clip_audio.wav). Clip time = match
time - T0 (the clip's first frame, from clip.log). Events from clip_timeline.json. Ironhail's shape.
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
jump = lambda f, t, L=0.06: db(g(f, t, t + L)) - db(g(f, t - L, t))
ev = json.load(open(S / "clip_timeline.json"))
NOTES = [440 * 2 ** (s / 12) for s in (0, 3, 7, 12)]            # the cast's A C E A
TOUCH = [220 * 2 ** (s / 12) for s in (0, 3, 5, 7, 10)]         # the snap's note at counts 1-5
print(f"CLIP {sys.argv[1]}  {n / sr:.2f}s  first frame at match {T0:.3f}")
cast = [e for e in ev if e[0] == "cast"][0][1] - T0
print(f"CAST at clip {cast:.3f}: each of A C E A (440 / 523 / 659 / 880 Hz) at its own onset, a note every 125 ms --")
print("  its band in the 60 ms from its onset against the 60 ms before")
for k, f in enumerate(NOTES):
    t = cast + 0.125 * k
    print(f"  note {k + 1}  {f:6.1f} Hz at {t:6.3f}s  {jump(f, t):+5.1f} dB")
print("TOUCHES: the snap's note for the count it was played at (220 x the pentatonic step), and the hex-snap's")
print("         2.6 kHz band, the 60 ms from the touch against the 60 ms before")
for e in ev:
    if e[0] != "touch": continue
    t, k = e[1] - T0, e[2]; f = TOUCH[min(max(k, 1), 5) - 1]
    print(f"  n{k} at {t:6.3f}s  note {f:6.1f} Hz {jump(f, t):+5.1f} dB   its square's 3rd {3 * f:6.1f} Hz {jump(3 * f, t):+5.1f} dB   "
          f"hex-snap 2600 Hz {jump(2600, t):+5.1f} dB   walls {e[3]}")
cl = [e for e in ev if e[0] == "close"]
if cl:
    t = cl[0][1] - T0
    print(f"CLOSE at clip {t:.3f} ({cl[0][3]}): MIRROR -- the notes swell and drop out top first, the root last (it cuts ~0.60s")
    print("  after the close). Each note's band over the last 0.1 s of its swell (up to its cut), against the 0.3 s before the close:")
    for k, f in enumerate(NOTES):
        c = 0.375 + 0.228 - k * 0.125
        a, b = t + max(0.0, c - 0.1), t + c
        print(f"  note {k + 1}  {f:6.1f} Hz  {a:6.3f}-{b:6.3f}s  {db(g(f, a, b)) - db(g(f, t - 0.3, t)):+5.1f} dB")
    print("  the level around it (dBFS, 100 ms spans):")
    for a in (t - 0.2, t - 0.1, t, t + 0.1, t + 0.2, t + 0.3, t + 0.4, t + 0.5, t + 0.6, t + 0.7):
        print(f"    {a:6.2f}-{a + 0.1:6.2f}s  {db(rms(a, a + 0.1)):6.1f} dBFS   440 Hz {db(g(440, a, a + 0.1)):6.1f}")
