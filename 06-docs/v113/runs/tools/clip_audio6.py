"""The clip's own audio against the same window filmed on the stage-5 link (the b26.5: its cast plays the freeze's
creak and cinch, and a bramble, a snare and a bite play nothing), both decoded from their AAC to mono 48 kHz. Each
stage-6 voice read in its own band over its own time, with and without: a voice that is in the mix reads above the
same window without it. Control: the same readings at match times with no stage-6 voice sounding must come back
near 0 dB (the two clips are the same fight, frame for frame: engine_ab, and the end states agree).
    python clip_audio6.py <clipwork dir> <timeline txt> <T0: the clip's first frame, match time> <clip sha16> <base sha16>"""
import numpy as np, wave, re, sys, pathlib
W, TL, T0 = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), float(sys.argv[3])
def load(p):
    w = wave.open(str(p)); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0, w.getframerate()
x, sr = load(W / "clip.wav"); y, _ = load(W / "base.wav")
n = min(len(x), len(y)); x, y = x[:n], y[:n]
DUR = n / sr
def band(sig, t0, t1, f0, f1):
    a, b = int(t0 * sr), int(t1 * sr)
    seg = sig[a:b] * np.hanning(b - a)
    sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(b - a, 1 / sr)
    return 10 * np.log10(sp[(fr >= f0) & (fr < f1)].sum() + 1e-12)
def row(name, t, a, b, f0, f1, quiet=False):
    v = t - T0
    if v + b > DUR or v + a < 0: return None
    d = band(x, v + a, v + b, f0, f1) - band(y, v + a, v + b, f0, f1)
    if not quiet: print(f"  {name:44s} match {t:7.3f}  video {v:6.3f}  {f0:>5}-{f1:<5} Hz  with - without {d:+6.1f} dB")
    return d
tl = TL.read_text(encoding="utf-8")
def times(pat): return [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s.*" + pat, tl, re.M)]
CAST = times(r"CAST")[0]
PLANT = times(r"thornwake-crackle")
SNARE = times(r"thornwake-snare")
BITE = times(r"thornwake-bite")
print(f"clip {sys.argv[4]} (the fx link) against clip_base {sys.argv[5]} (the b26.5), the same window; the clip's first frame "
      f"at match {T0}, {DUR:.2f} s of audio")
print(f"the timeline: the cast at {CAST}, {len(PLANT)} crackles, {len(SNARE)} snares, {len(BITE)} bites in the clip")
row("the cast's rustle (the needles, 2.4-3.9 kHz)", CAST, 0.05, 0.35, 2400, 3900)
row("the cast's creak (the 330 Hz timber)", CAST, 0.05, 0.35, 320, 340)
def summary(name, ts, a, b, f0, f1):
    ds = [d for d in (row(name, t, a, b, f0, f1, quiet=True) for t in ts) if d is not None]
    if ds: print(f"  the {len(ds)} {name}: min {min(ds):+.1f}, median {np.median(ds):+.1f}, max {max(ds):+.1f} dB")
    return ds
dc = summary("crackles (1.2-2.2 kHz, 100-280 ms after, past the blow's body)", PLANT, 0.10, 0.28, 1200, 2200)
dsn = summary("snares' creak (the 260 Hz timber, 0-190 ms)", SNARE, 0.0, 0.19, 250, 270)
dsc = summary("snares' crack (the highpass over 2.6 kHz, 200-235 ms)", SNARE, 0.20, 0.235, 2600, 12000)
db = summary("bites (the 420-620 Hz sweep, 0-100 ms)", BITE, 0.0, 0.10, 400, 650)
print("CONTROL -- the same bands at match times with no stage-6 voice sounding (must come back near 0):")
q = [T0 + 0.10, T0 + 0.45]
cs = [row("before the cast, " + nm, t, a, b, f0, f1) for t in q
      for nm, a, b, f0, f1 in (("the rustle band", 0.05, 0.35, 2400, 3900), ("the crackle band", 0.10, 0.28, 1200, 2200),
                               ("the timber band", 0.0, 0.19, 250, 270), ("the bite band", 0.0, 0.10, 400, 650))]
cs = [c for c in cs if c is not None]
cm = max(abs(c) for c in cs)
print(f"  no-voice controls: max |d| {cm:.1f} dB")
for nm, ds in (("crackles", dc), ("snares' creak", dsn), ("snares' crack", dsc), ("bites", db)):
    if ds: print(f"  the {nm} over the no-voice spread ({cm:.1f} dB): {sum(d > cm for d in ds)} of {len(ds)}")
