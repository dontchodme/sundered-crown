"""The clip's own audio against the same window filmed on the stage-5 link (the b7.5: no stage-6 voice; its cast
plays rune-crack, a proc plays nothing, a close nothing), both decoded from their AAC to mono 48 kHz. Each
stage-6 voice read in its own band over its own time, with and without: a voice that is in the mix reads above
the same window without it. Control: the same readings at match times with no stage-6 voice sounding must come
back near 0 dB (the two clips are the same fight, frame for frame: engine_ab, and the end states agree).
    python clip_audio6.py <clipwork dir> <clip sha16> <base sha16>"""
import numpy as np, wave, re, sys, pathlib
W = pathlib.Path(sys.argv[1])
def load(p):
    w = wave.open(str(p)); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0, w.getframerate()
x, sr = load(W / "clip.wav"); y, _ = load(W / "base.wav")
n = min(len(x), len(y)); x, y = x[:n], y[:n]
T0 = 77.98333      # the clip's first frame, match time (cinema_clip's log); the clip plays 1:1 (766 frames, 12.77 s)
def band(sig, t0, t1, f0, f1):
    a, b = int(t0 * sr), int(t1 * sr)
    seg = sig[a:b] * np.hanning(b - a)
    sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(b - a, 1 / sr)
    return 10 * np.log10(sp[(fr >= f0) & (fr < f1)].sum() + 1e-12)
def row(name, t, a, b, f0, f1, quiet=False):
    v = t - T0
    d = band(x, v + a, v + b, f0, f1) - band(y, v + a, v + b, f0, f1)
    if not quiet: print(f"  {name:40s} match {t:7.3f}  video {v:6.3f}  {f0:>5}-{f1:<5} Hz  with - without {d:+6.1f} dB")
    return d
print(f"clip {sys.argv[2]} (the fx link) against clip_base {sys.argv[3]} (the b7.5), Spellbreaker v Vesper 111075, the same window")
tl = (W.parent.parent / "runs" / "stage6_clip_timeline.txt").read_text(encoding="utf-8")
STUNS = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s.*spellbreaker-stun", tl, re.M)]
CAST = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s+CAST", tl, re.M)][0]
CLOSE = [float(m.group(1)) for m in re.finditer(r"^\s+([\d.]+)\s+CLOSE by the clock", tl, re.M)][0]
d_cast_hum = row("the cast's hum (C4, 0.12-0.40 s)", CAST, 0.12, 0.40, 252, 272)
d_cast_crk = row("the cast's crack (the glass at G6, 0-60 ms)", CAST, 0.0, 0.06, 1450, 1700)
ds = [row("a stun's tail (the 2.6 kHz sizzle, 60-300 ms)", t, 0.06, 0.30, 2400, 2800, quiet=True) for t in STUNS]
print(f"  the {len(ds)} stun voices' tails (2400-2800 Hz, 60-300 ms after each): min {min(ds):+.1f}, median {np.median(ds):+.1f}, max {max(ds):+.1f} dB")
d_close = row("the close (the hum held, 0-0.2 s)", CLOSE, 0.0, 0.2, 252, 272)
print("CONTROL -- the same readings at match times with no stage-6 voice sounding (must come back near 0):")
CT = [("C4 band, before the cast", t, 0.0, 0.28, 252, 272) for t in (78.10, 78.55)]
CT += [("C4 band, after the close's hum", t, 0.0, 0.28, 252, 272) for t in (89.45, 89.90, 90.30)]
CT += [("sizzle band, before the cast", t, 0.06, 0.30, 2400, 2800) for t in (78.10, 78.55)]
CT += [("sizzle band, after the last stun", t, 0.06, 0.30, 2400, 2800) for t in (89.45, 89.90, 90.30)]
cs = [row(*e) for e in CT]
print(f"  no-voice controls: max |d| {max(abs(c) for c in cs):.1f} dB (the C4 band {max(abs(c) for c in cs[:5]):.1f}, the sizzle band {max(abs(c) for c in cs[5:]):.1f})")
cmax = max(abs(c) for c in cs[5:])
print(f"  the stun tails over the sizzle band's no-voice spread ({cmax:.1f} dB): {sum(d > cmax for d in ds)} of {len(ds)}")
print("  (the two renders differ everywhere at about -40 dB broadband, some 18 dB under the mix, before the cast too -- "
      "not traced here; the sizzle band, where the hits' noise lives, carries that spread, and the C4 band does not)")
print("  (the crack's row compares it to the b7.5's own cast voice, rune-crack, on the same frames -- loud, its centroid "
      "3.2 kHz -- not to silence)")
