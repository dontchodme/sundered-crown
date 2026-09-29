"""The clip's own audio against the same window filmed on the stage-5 link (b12.5: no stage-6 voice; its cast
plays rune-crack), both decoded from their AAC to mono 48 kHz. Each stage-6 voice read in its own band over its
own time, with and without: a voice that is in the mix reads above the same window without it. Control: the same
readings at match times with no stage-6 voice must come back near 0 dB (the two clips are the same fight,
frame for frame: engine_ab)."""
import numpy as np, wave
def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0, w.getframerate()
x, sr = load("clipwork/clip.wav"); y, _ = load("clipwork/base.wav")
n = min(len(x), len(y)); x, y = x[:n], y[:n]
T0 = 43.625          # the clip's first frame, match time; the clip plays 1:1 (735 frames for 12.25 s)
def band(sig, t0, t1, f0, f1):
    a, b = int(t0 * sr), int(t1 * sr)
    seg = sig[a:b] * np.hanning(b - a)
    sp = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(b - a, 1 / sr)
    return 10 * np.log10(sp[(fr >= f0) & (fr < f1)].sum() + 1e-12)
def row(name, t, a, b, f0, f1):
    v = t - T0
    d = band(x, v + a, v + b, f0, f1) - band(y, v + a, v + b, f0, f1)
    print(f"  {name:36s} match {t:7.3f}  video {v:6.3f}  {f0:>5}-{f1:<5} Hz  with - without {d:+6.1f} dB")
    return d
print(f"clip f56af7299f6f5072 (the fx link) against clip_base {open('clip_base.sha').read().strip()} (the b12.5), same window")
EV = [("the cast (the swell, 0.20-0.45 s)", 44.817, 0.20, 0.45, 240, 420)]
EV += [("an entry (C6, first 100 ms)", t, 0.0, 0.1, 990, 1110) for t in (46.292, 47.550, 48.183, 48.567, 49.258, 50.717, 52.850, 53.350)]
EV += [("a heal chime (spark collect, 135 ms)", t, 0.0, 0.135, 1240, 1780) for t in (44.817, 46.292, 47.550, 48.567, 49.375, 50.417, 51.458, 52.850)]
EV += [("the close (0-0.5 s)", 54.058, 0.0, 0.5, 240, 420)]
ds = [row(*e) for e in EV]
print("  (the chime on the CAST's frame reads against the base's own cast voice, rune-crack -- centroid 3.2 kHz, loud --")
print("   which the fx link replaced with the swell: that one row compares the chime to rune-crack, not to silence)")
rest = [d for e, d in zip(EV, ds) if not (e[0].startswith("a heal chime") and e[1] == 44.817)]
print(f"  every other stage-6 event ({len(rest)}): min {min(rest):+.1f} dB, median {np.median(rest):+.1f} dB")
print("CONTROL -- the same readings at match times with no stage-6 voice (must come back near 0):")
CT = [("C6 band, no entry", t, 0.0, 0.1, 990, 1110) for t in (45.60, 51.90, 52.40, 54.90, 55.40)]
CT += [("chime band, no blessing", t, 0.0, 0.135, 1240, 1780) for t in (45.60, 51.90, 54.90)]
CT += [("C4-G4 band, no swell", t, 0.0, 0.5, 240, 420) for t in (51.00, 55.20)]
cs = [row(*e) for e in CT]
print(f"  no-voice controls: max |d| {max(abs(c) for c in cs):.1f} dB")
