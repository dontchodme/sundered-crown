"""The clip's audio, read for the four voices: the sigil's E7 line (2640 Hz) in the window and not after the close,
and the loudness around the cast, the snaps and the close (video times from runs/stage6_clip_events.txt)."""
import sys, subprocess, numpy as np
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from clip_spread import resolve_ffmpeg
CLIP = "C:/dev/sundered-crown/07-shorts/v105/foresight-window.mp4"
SR = 48000
raw = subprocess.run([resolve_ffmpeg(), "-v", "error", "-i", CLIP, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
print(f"CLIP {CLIP}  {len(x)/SR:.2f}s mono {SR} Hz")
def line(t0, t1, f=2640.0):
    """power in the 2640 Hz line (+-4 Hz) against the median of the 2400-2900 Hz band (a tone stands out of it)"""
    seg = x[int(t0*SR):int(t1*SR)] * np.hanning(int(t1*SR)-int(t0*SR))
    P = np.abs(np.fft.rfft(seg))**2; fr = np.fft.rfftfreq(len(seg), 1/SR)
    on = P[(fr > f-4) & (fr < f+4)].max(); band = np.median(P[(fr > 2400) & (fr < 2900)])
    return 10*np.log10(on/band), 10*np.log10(on/len(seg)+1e-30)
print("THE SIGIL'S LINE, 2640 Hz, over the median of 2.4-2.9 kHz (a tone stands tens of dB out of it):")
for name, a, b in [("before the cast   0.00-1.15", 0.0, 1.15), ("window, early     1.60-5.60", 1.6, 5.6),
                   ("window, late      5.60-10.50", 5.6, 10.5), ("after the close  11.00-12.30", 11.0, 12.3)]:
    r, lv = line(a, b); print(f"  {name}:  line {r:+6.1f} dB over the band")
def rms(t0, t1):
    s = x[int(t0*SR):int(t1*SR)]; return 20*np.log10(np.sqrt(np.mean(s*s))+1e-12)
print("LOUDNESS (RMS dBFS, 50 ms) at each voice's frame against the 150 ms before it:")
for name, t in [("cast   1.20", 1.203), ("snap n2 2.16", 2.162), ("snap n4 4.46", 4.462), ("snap n5 5.42", 5.42),
                ("snap n3 8.66", 8.662), ("close 10.55", 10.553)]:
    print(f"  {name}:  {rms(t, t+0.05):6.1f} dB  (before {rms(t-0.15, t):6.1f})")
def line2(t0, t1, f, lo, hi):
    seg = x[int(t0*SR):int(t1*SR)] * np.hanning(int(t1*SR)-int(t0*SR))
    P = np.abs(np.fft.rfft(seg))**2; fr = np.fft.rfftfreq(len(seg), 1/SR)
    return 10*np.log10(P[(fr > f-8) & (fr < f+8)].max() / np.median(P[(fr > lo) & (fr < hi)]))
print("THE CHIME'S BAR MODE, 2640 x 2.76 = 7286 Hz (only the cast and the close carry it; the sigil is a pure 2640):")
for name, a, b in [("before the cast   0.60-1.10", 0.6, 1.1), ("the cast's chime  1.45-1.95", 1.45, 1.95),
                   ("mid-window        5.00-5.50", 5.0, 5.5), ("mid-window        9.00-9.50", 9.0, 9.5),
                   ("the close         10.50-11.00", 10.5, 11.0), ("after the close   11.30-11.80", 11.3, 11.8)]:
    print(f"  {name}:  line {line2(a, b, 2640*2.76, 6800, 7800):+6.1f} dB over the 6.8-7.8 kHz band")
