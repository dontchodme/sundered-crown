"""v114 scratch: the clip's own audio against the same window filmed on the stage-5 link (the b10.25: no stage-6
voice -- its cast plays rune-crack, a priced blow the plain strike), both decoded from their AAC to mono 48 kHz.
The two clips are the same fight frame for frame (engine_ab, and the timeline), so a difference at an event is
the voice. Read where each voice is:
  THE CAST: the draw's scrape RISES (the power centroid at 2-12 kHz, its first 100 ms against its last, cents),
            where rune-crack falls; and the drops (700-1600 Hz, 0.15-0.45 s after the cast) with and without;
  A PRICED BLOW: the strike's body (the FFT peak at 40-400 Hz over the first 40 ms, cents, with vs without):
            down by about 100 c a stack; the plain blows (window shut, or n 0) the CONTROL, near 0;
  THE CLOSE: nothing -- the window's close, with and without, near 0 dB in every band.
    python clip_audio6.py <clipwork dir> <timeline txt> <T0, the clip's first frame in match time>"""
import numpy as np, re, sys, wave, pathlib
W = pathlib.Path(sys.argv[1]); tl = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"); T0 = float(sys.argv[3])


def load(p):
    w = wave.open(str(p)); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0, w.getframerate()


x, sr = load(W / "clip.wav"); y, _ = load(W / "base.wav")
n = min(len(x), len(y)); x, y = x[:n], y[:n]


def seg(sig, t0, t1):
    a, b = int((t0 - T0) * sr), int((t1 - T0) * sr)
    return sig[a:b] * np.hanning(b - a)


def power(sig, t0, t1, f0, f1):
    s = seg(sig, t0, t1); sp = np.abs(np.fft.rfft(s)) ** 2; fr = np.fft.rfftfreq(len(s), 1 / sr)
    return sp[(fr >= f0) & (fr < f1)].sum() + 1e-12


def db(sig, t0, t1, f0, f1):
    return 10 * np.log10(power(sig, t0, t1, f0, f1))


def centroid(sig, t0, t1, f0, f1):
    s = seg(sig, t0, t1); sp = np.abs(np.fft.rfft(s, 8 * len(s))) ** 2; fr = np.fft.rfftfreq(8 * len(s), 1 / sr)
    k = (fr >= f0) & (fr < f1); return (sp[k] * fr[k]).sum() / (sp[k].sum() + 1e-30)


def peak(sig, t0, t1, f0, f1):
    s = seg(sig, t0, t1); N = 32 * len(s); sp = np.abs(np.fft.rfft(s, N)); fr = np.fft.rfftfreq(N, 1 / sr)
    k = np.where((fr >= f0) & (fr < f1))[0]; return fr[k[np.argmax(sp[k])]]


cents = lambda a, b: 1200 * np.log2(a / b)
CAST = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s+CAST voice", tl, re.M)][0]
CLOSE = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s+WINDOW CLOSES by the clock", tl, re.M)][0]
PR = [(float(m.group(1)), int(m.group(2))) for m in re.finditer(r"^\s+([\d.]+)\s+PRICED blow voice: price (\d)", tl, re.M)]
PL = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s+her plain blow voice", tl, re.M)]
print(f"the clip against the same window on the stage-5 link; the clip's first frame at match {T0:.3f}")
print(f"THE CAST at {CAST:.3f}:")
for name, sig in (("with (DRIP)", x), ("without (rune-crack)", y)):
    c0, c1 = centroid(sig, CAST, CAST + 0.1, 2000, 12000), centroid(sig, CAST + 0.3, CAST + 0.4, 2000, 12000)
    print(f"  {name:22s} the 2-12 kHz centroid {c0:6.0f} Hz in its first 100 ms -> {c1:6.0f} Hz in its last: {cents(c1, c0):+5.0f} c")
d = db(x, CAST + 0.15, CAST + 0.45, 700, 1600) - db(y, CAST + 0.15, CAST + 0.45, 700, 1600)
print(f"  the drops' band (700-1600 Hz, 0.15-0.45 s): with - without {d:+.1f} dB")
d = db(x, CAST + 0.2, CAST + 0.45, 4000, 9000) - db(y, CAST + 0.2, CAST + 0.45, 4000, 9000)
print(f"  the scrape's top (4-9 kHz, 0.20-0.45 s): with - without {d:+.1f} dB")
print("A PRICED BLOW: the strike's body, the FFT peak at 40-400 Hz over its first 40 ms, with against without:")
rows = []
for t, k in PR:
    pw, pb = peak(x, t, t + 0.04, 40, 400), peak(y, t, t + 0.04, 40, 400)
    rows.append((k, cents(pw, pb)))
    print(f"  {t:8.3f}  n {k}   {pb:6.1f} Hz -> {pw:6.1f} Hz   {cents(pw, pb):+5.0f} c   (the arm: {-100 * k:+d} c)")
print("CONTROL -- her plain blows (the same call on both links), the same reading, must come back near 0:")
for t in PL:
    pw, pb = peak(x, t, t + 0.04, 40, 400), peak(y, t, t + 0.04, 40, 400)
    print(f"  {t:8.3f}  plain  {pb:6.1f} Hz -> {pw:6.1f} Hz   {cents(pw, pb):+5.0f} c")
print(f"THE CLOSE at {CLOSE:.3f} (\"close -- nothing\"): with - without, 0-0.4 s:")
for f0, f1 in ((40, 400), (700, 1600), (2000, 12000)):
    print(f"  {f0:>5}-{f1:<5} Hz  {db(x, CLOSE, CLOSE + 0.4, f0, f1) - db(y, CLOSE, CLOSE + 0.4, f0, f1):+5.1f} dB")
print("CONTROL -- 0.5 s before the cast, the same bands: must come back near 0:")
for f0, f1 in ((40, 400), (700, 1600), (2000, 12000)):
    print(f"  {f0:>5}-{f1:<5} Hz  {db(x, CAST - 0.6, CAST - 0.2, f0, f1) - db(y, CAST - 0.6, CAST - 0.2, f0, f1):+5.1f} dB")
print("CONTROL -- windows after the first new voice with none of the three sounding (0.5 s clear of every event in the"
      " timeline), the same bands: what the AAC encode alone moves once the two soundtracks differ anywhere:")
EV = sorted([CAST, CLOSE] + [t for t, _ in PR] + PL)
cands = [t0 for t0 in np.arange(CAST + 1.0, CLOSE + 1.0, 0.05) if all(abs(t0 - e) > 0.5 and abs(t0 + 0.4 - e) > 0.5 for e in EV)]
picks = cands[::max(1, len(cands) // 4)][:4]
for t0 in picks:
    print(f"  {t0:8.3f}  " + "  ".join(f"{f0}-{f1} Hz {db(x, t0, t0 + 0.4, f0, f1) - db(y, t0, t0 + 0.4, f0, f1):+5.1f} dB"
                                       for f0, f1 in ((40, 400), (700, 1600), (2000, 12000))))
