"""The trailer's score: 30s, 128 BPM, D minor, synthesized from nothing (no samples,
no licence to read). Structure is locked to the edit's bar grid (see trailer_edit.py):

  bars 0-1   0.000- 3.750  cold open: two braams, clock ticks, riser
  bars 2-3   3.750- 7.500  half-time drums, filtered ostinato
  bars 4-7   7.500-15.000  full groove, Dm Bb F C
  bars 8-9  15.000-18.750  build: snare roll, riser, filter sweep, gap
  bar  10   18.750-20.625  THE STOP: impact, sub, reverse whoosh
  bars 11-12 20.625-24.375 final drop
  bars 13-15 24.375-30.000 title: impact, held chord under the voice, last hit 28.125
"""
import pathlib
import numpy as np
import soundfile as sf
from scipy import signal

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent / "07-shorts" / "worldcup-trailer"      # every render product lives here (mp4/wav gitignored)

SR = 48000
BPM = 128.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
DUR = 30.0
N = int(DUR * SR)
rng = np.random.default_rng(49)

L = np.zeros(N); R = np.zeros(N)
bus = {k: np.zeros((2, N)) for k in ("drums", "bass", "synth", "fx", "pad")}


def t_of(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def add(name, x, t0, gain=1.0, pan=0.0):
    """Mix mono or stereo x into a bus at t0 seconds."""
    i0 = int(round(t0 * SR))
    if x.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        x = np.vstack([x * l * np.sqrt(2), x * r * np.sqrt(2)])
    if i0 < 0:
        x = x[:, -i0:]; i0 = 0
    n = min(x.shape[1], N - i0)
    if n > 0:
        bus[name][:, i0:i0 + n] += gain * x[:, :n]


def env_ad(n, a, d, curve=4.0):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) * curve / max(d, 1e-6)))
    return e


def polyblep_saw(freq, n, phase0=0.0):
    f = np.broadcast_to(np.asarray(freq, dtype=float), (n,))
    dt = f / SR
    ph = (phase0 + np.cumsum(dt)) % 1.0
    y = 2 * ph - 1
    # polyBLEP
    m1 = ph < dt
    t1 = ph[m1] / dt[m1]
    y[m1] -= t1 + t1 - t1 * t1 - 1
    m2 = ph > 1 - dt
    t2 = (ph[m2] - 1) / dt[m2]
    y[m2] -= t2 * t2 + t2 + t2 + 1
    return y


def supersaw(freq, n, voices=7, detune=0.18, stereo=True):
    offs = np.linspace(-1, 1, voices) * detune  # semitones
    out = np.zeros((2, n))
    for i, o in enumerate(offs):
        s = polyblep_saw(freq * 2 ** (o / 12), n, rng.random())
        p = (i / (voices - 1)) * 2 - 1 if stereo else 0
        out[0] += s * np.cos((p + 1) * np.pi / 4)
        out[1] += s * np.sin((p + 1) * np.pi / 4)
    return out / np.sqrt(voices)


def sweep_filter(x, f0, f1, kind="lowpass", q=0.707, block=256, curve="exp"):
    """Block-wise time-varying biquad (state carried)."""
    x = np.atleast_2d(x)
    n = x.shape[1]
    out = np.zeros_like(x)
    nb = int(np.ceil(n / block))
    zi = None
    for b in range(nb):
        u = b / max(nb - 1, 1)
        fc = f0 * (f1 / f0) ** u if curve == "exp" else f0 + (f1 - f0) * u
        fc = min(max(fc, 20), SR * 0.45)
        sos = signal.butter(2, fc, btype=kind, fs=SR, output="sos")
        if zi is None:
            zi = np.zeros((x.shape[0], sos.shape[0], 2))
        seg = x[:, b * block:(b + 1) * block]
        for c in range(x.shape[0]):
            out[c, b * block:(b + 1) * block], zi[c] = signal.sosfilt(sos, seg[c], zi=zi[c])
    return out


def filt(x, fc, kind="lowpass", order=2):
    sos = signal.butter(order, fc, btype=kind, fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=-1)


def noise(n):
    return rng.standard_normal(n)


# ---------------------------------------------------------------- instruments
def kick(level=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7.5)
    click = filt(noise(n), 3000, "highpass") * np.exp(-t * 300) * 0.5
    return np.tanh(1.6 * (body + click)) * level


def clap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    e = np.zeros(n)
    for k, d in enumerate([0, 0.009, 0.018, 0.028]):
        i = int(d * SR); e[i:] += np.exp(-(t[:n - i]) * (160 if k < 3 else 22))
    x = signal.sosfilt(signal.butter(2, [900, 5200], btype="band", fs=SR, output="sos"), noise(n)) * e
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.4
    return (x * 1.6 + body)


def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR); t = np.arange(n) / SR
    x = filt(noise(n), 7000, "highpass", 4) * np.exp(-t * (14 if open_ else 70))
    return x * 0.5


def snare():
    n = int(0.3 * SR); t = np.arange(n) / SR
    x = filt(noise(n), 1500, "highpass") * np.exp(-t * 20)
    body = np.sin(2 * np.pi * (180 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 25)
    return x * 0.9 + body * 0.6


def tom(f=90):
    n = int(0.6 * SR); t = np.arange(n) / SR
    ff = f * (1 + 0.6 * np.exp(-t * 18))
    x = np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 6)
    x += filt(noise(n), 400, "lowpass") * np.exp(-t * 40) * 0.8
    return np.tanh(1.4 * x)


def impact(size=1.0):
    """Sub boom + noise crack + metal ring."""
    n = int(3.5 * SR); t = np.arange(n) / SR
    f = 32 + 90 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    crack = filt(noise(n), 900, "highpass") * np.exp(-t * 18) * 0.8
    ring = sum(np.sin(2 * np.pi * fr * t + rng.random() * 6) * np.exp(-t * dk)
               for fr, dk in [(211, 3), (347, 4), (523, 5), (811, 6)]) * 0.06
    return np.tanh(1.8 * (boom * 1.2 + crack + ring)) * size


def braam(root=36.71, dur=2.6, bright=1.0):
    """Low brass-like blast: stacked detuned saws, fast filter open, slow close, saturated."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros((2, n))
    for mult, g in [(1, 1.0), (2, 0.8), (3, 0.45), (4, 0.3)]:   # root, octave, fifth-ish, 2 oct
        fr = root * (1.5 if mult == 3 else mult)
        x += supersaw(fr, n, voices=5, detune=0.12) * g
    e = np.minimum(1, t / 0.03) * np.exp(-t * 0.9)
    y = sweep_filter(x * e, 2400 * bright, 180, "lowpass", block=512)
    return np.tanh(2.2 * y) * 0.7


def riser(dur, f0=300, f1=9000):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sweep_filter(noise(n), f0, f1, "lowpass", block=256)[0]
    x = filt(x, 200, "highpass")
    tone = polyblep_saw(110 * 2 ** (3 * t / dur), n) * 0.25
    tone = filt(tone, 3000)
    e = (t / dur) ** 2.2
    return (x * 0.9 + tone) * e


def reverse_whoosh(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = filt(noise(n), 2500, "highpass")
    e = (t / dur) ** 3
    return x * e * 0.8


def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 280) * 0.5 + filt(noise(n), 5000, "highpass") * np.exp(-t * 400) * 0.3


def crash():
    n = int(2.8 * SR); t = np.arange(n) / SR
    x = filt(noise(n), 4500, "highpass", 2) * np.exp(-t * 1.6)
    x += filt(noise(n), 9000, "highpass", 2) * np.exp(-t * 3) * 0.5
    return x * 0.45


# ---------------------------------------------------------------- harmony
NOTE = lambda midi: 440.0 * 2 ** ((midi - 69) / 12)
D2, F2, A2, Bb1, C2 = 38, 41, 45, 34, 36
CHORDS = {  # root midi (bass), triad midi (pad)
    "Dm": (38, [62, 65, 69]),
    "Bb": (34, [58, 62, 65]),
    "F":  (41, [60, 65, 69]),
    "C":  (36, [60, 64, 67]),
}


def pad(chord, dur, level=1.0, bright=2400):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros((2, n))
    for m in CHORDS[chord][1]:
        x += supersaw(NOTE(m), n, voices=7, detune=0.22)
    x += supersaw(NOTE(CHORDS[chord][1][0] - 12), n, voices=5, detune=0.15) * 0.6
    e = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05).clip(0, 1)
    return filt(x * e, bright) * 0.28 * level


def bass_note(chord, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = NOTE(CHORDS[chord][0])
    x = polyblep_saw(f, n) * 0.6 + np.sin(2 * np.pi * f * t) * 0.8
    e = np.minimum(1, t / 0.004) * np.exp(-t * 3.5)
    return np.tanh(1.5 * filt(x * e, 700))


OST = [0, 12, 7, 12, 3, 12, 7, 10]  # semitones over chord root (in the octave above the pad)


def ostinato_bar(chord, bar, level, cutoff0, cutoff1, octave=0):
    root = CHORDS[chord][1][0] - 12 + 12 * octave  # D4 region -> D3
    step = BEAT / 4
    n = int(step * SR * 0.9)
    for i in range(16):
        m = root + OST[i % 8] + (3 if chord in ("Dm",) and OST[i % 8] == 3 else 0) * 0
        fr = NOTE(m)
        x = supersaw(fr, n, voices=3, detune=0.08)
        t = np.arange(n) / SR
        x = x * np.exp(-t * 18)
        cf = cutoff0 * (cutoff1 / cutoff0) ** (i / 15)
        x = filt(x, cf)
        add("synth", x, t_of(bar, i / 4), level * (1.0 if i % 4 == 0 else 0.75))


# ---------------------------------------------------------------- arrangement
# A) cold open
add("fx", braam(NOTE(26), 3.2), 0.0, 0.9)
add("fx", impact(0.8), 0.0, 0.9)
add("fx", braam(NOTE(26), 2.4, bright=1.3), t_of(1), 0.95)
add("fx", impact(0.6), t_of(1), 0.7)
for i in range(16):
    add("drums", tick(), t_of(0, i / 2), 0.35 + 0.02 * i, pan=0.3 if i % 2 else -0.3)
add("fx", riser(1.6), t_of(1, 0.6), 0.55)
# one bright pop per row of the wall as it ignites (trailer_gfx.wall: a row per sixteenth from 0.12s)
def pop(f):
    n = int(0.16 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 32) + filt(noise(n), 4000, "highpass") * np.exp(-t * 160) * 0.4) * 0.8
for r in range(7):
    add("fx", pop(740 * 2 ** (2 * r / 12)), 0.12 + r * BEAT / 4, 0.45, pan=(r - 3) / 4)
add("fx", reverse_whoosh(0.9), t_of(2) - 0.9, 0.6)
drone_n = int(t_of(2) * SR)
tt = np.arange(drone_n) / SR
drone = (polyblep_saw(NOTE(26), drone_n) + polyblep_saw(NOTE(33), drone_n) * 0.6)
drone = filt(drone, 220) * np.minimum(1, tt / 0.8) * 0.35
add("bass", drone, 0.0)

# B) half-time, bars 2-3
for bar in (2, 3):
    add("drums", kick(), t_of(bar, 0), 0.9)
    add("drums", snare(), t_of(bar, 2), 0.7)
    add("drums", tom(95), t_of(bar, 3), 0.4, pan=-0.2)
    add("drums", tom(75), t_of(bar, 3.5), 0.4, pan=0.2)
    for i in range(8):
        add("drums", hat(), t_of(bar, i / 2), 0.25, pan=0.25)
    ch = "Dm" if bar == 2 else "Bb"
    ostinato_bar(ch, bar, 0.30, 500, 1400)
    add("pad", pad(ch, BAR, 0.55, 1200), t_of(bar))
    add("bass", bass_note(ch, BAR * 0.9), t_of(bar), 0.7)
add("fx", crash(), t_of(2), 0.6)

# C) full groove, bars 4-7
prog = ["Dm", "Bb", "F", "C"]
for j, bar in enumerate(range(4, 8)):
    ch = prog[j]
    for b in range(4):
        add("drums", kick(), t_of(bar, b), 1.0)
        for s in (0.5,):
            add("drums", hat(), t_of(bar, b + s), 0.4, pan=0.3)
        add("drums", hat(), t_of(bar, b + 0.25), 0.15, pan=-0.3)
        add("drums", hat(), t_of(bar, b + 0.75), 0.15, pan=-0.3)
        add("bass", bass_note(ch, BEAT * 0.45), t_of(bar, b + 0.5), 0.8)
        add("bass", bass_note(ch, BEAT * 0.4), t_of(bar, b), 0.6)
    add("drums", clap(), t_of(bar, 1), 0.75)
    add("drums", clap(), t_of(bar, 3), 0.75)
    ostinato_bar(ch, bar, 0.42, 1400, 3200)
    add("pad", pad(ch, BAR, 0.9, 2600), t_of(bar))
add("fx", impact(0.7), t_of(4), 0.8)
add("fx", crash(), t_of(4), 0.8)
add("fx", impact(0.45), t_of(5), 0.55)
add("fx", crash(), t_of(6), 0.45)

# D) build, bars 8-9 (the last half beat of bar 9 is silence)
for bar, ch in ((8, "Bb"), (9, "C")):
    for b in range(4):
        if bar == 9 and b == 3:
            break
        add("drums", kick(), t_of(bar, b), 0.95)
    ostinato_bar(ch, bar, 0.45, 2000 if bar == 8 else 3500, 3500 if bar == 8 else 7000)
    add("pad", pad(ch, BAR if bar == 8 else BAR - BEAT, 0.9, 3000 if bar == 8 else 4000), t_of(bar))
    add("bass", bass_note(ch, BAR * 0.7), t_of(bar), 0.7)
# snare roll: 8ths bar 8 beats 2-4, 16ths bar 9 beats 0-2, 32nds last beat before the gap
roll = [t_of(8, 2 + i / 2) for i in range(4)] + [t_of(9, i / 4) for i in range(8)] + [t_of(9, 2 + i / 8) for i in range(8)]
for k, tr in enumerate(roll):
    add("drums", snare(), tr, 0.35 + 0.5 * k / len(roll), pan=(-0.15 if k % 2 else 0.15))
add("fx", riser(BAR * 2 - BEAT), t_of(8), 0.8)

# E) the stop, bar 10
add("fx", impact(1.2), t_of(10), 1.1)
add("fx", braam(NOTE(26), 3.4, bright=1.4), t_of(10), 1.0)
add("fx", crash(), t_of(10), 0.9)
add("drums", tom(60), t_of(10, 2), 0.55)
add("fx", reverse_whoosh(1.0), t_of(11) - 1.0, 0.8)
add("fx", riser(0.9, 800, 12000), t_of(11) - 0.9, 0.45)

# F) final drop, bars 11-12: chords every half bar
prog2 = ["Dm", "Bb", "F", "C"]
for j, bar in enumerate((11, 12)):
    for h in range(2):
        ch = prog2[j * 2 + h]
        add("pad", pad(ch, BAR / 2, 1.0, 5000), t_of(bar, 2 * h))
    for b in range(4):
        add("drums", kick(), t_of(bar, b), 1.05)
        for s in (0.25, 0.5, 0.75):
            add("drums", hat(s == 0.5), t_of(bar, b + s), 0.35 if s == 0.5 else 0.2, pan=0.3)
        ch = prog2[j * 2 + (b // 2)]
        add("bass", bass_note(ch, BEAT * 0.45), t_of(bar, b + 0.5), 0.9)
        add("bass", bass_note(ch, BEAT * 0.4), t_of(bar, b), 0.7)
    add("drums", clap(), t_of(bar, 1), 0.85)
    add("drums", clap(), t_of(bar, 3), 0.85)
    for h in range(2):
        ch = prog2[j * 2 + h]
        # ostinato in half-bar chunks
        root = CHORDS[ch][1][0] - 12
        for i in range(8):
            fr = NOTE(root + OST[i])
            n = int(BEAT / 4 * SR * 0.9); t = np.arange(n) / SR
            x = filt(supersaw(fr, n, 3, 0.08) * np.exp(-t * 16), 6000)
            add("synth", x, t_of(bar, 2 * h + i / 4), 0.45)
            x2 = filt(supersaw(fr * 2, n, 3, 0.1) * np.exp(-t * 20), 7000)
            add("synth", x2, t_of(bar, 2 * h + i / 4), 0.18)
add("fx", impact(1.0), t_of(11), 1.0)
add("fx", crash(), t_of(11), 1.0)
add("fx", crash(), t_of(12), 0.6)
add("fx", reverse_whoosh(0.8), t_of(13) - 0.8, 0.7)

# G) title, bars 13-15
add("fx", impact(1.3), t_of(13), 1.15)
add("fx", braam(NOTE(26), 3.8, bright=1.5), t_of(13), 1.0)
add("fx", crash(), t_of(13), 1.0)
add("pad", pad("Dm", BAR * 2, 0.8, 3200), t_of(13))
for bar in (13, 14):
    add("drums", kick(), t_of(bar, 0), 0.8)
    add("drums", snare(), t_of(bar, 2), 0.5)
    add("drums", tom(80), t_of(bar, 3.5), 0.35)
    ch = "Dm" if bar == 13 else "Bb"
    ostinato_bar(ch, bar, 0.28, 1200, 2400)
    add("bass", bass_note(ch, BAR * 0.9), t_of(bar), 0.6)
# last hit on bar 15, ring out
add("fx", impact(1.0), t_of(15), 1.0)
add("fx", braam(NOTE(26), 1.875, bright=1.1), t_of(15), 0.8)
add("pad", pad("Dm", 1.8, 0.7, 2600), t_of(15))

# ---------------------------------------------------------------- sidechain + reverb + master
kick_times = []
for bar in list(range(2, 4)):
    kick_times.append(t_of(bar, 0))
for bar in range(4, 9):
    kick_times += [t_of(bar, b) for b in range(4)]
kick_times += [t_of(9, b) for b in range(3)]
for bar in (11, 12):
    kick_times += [t_of(bar, b) for b in range(4)]
duck = np.ones(N)
tt = np.arange(N) / SR
for kt in kick_times:
    i = int(kt * SR); n = int(0.3 * SR)
    seg = 1 - 0.55 * np.exp(-np.arange(n) / SR * 14)
    duck[i:i + n] = np.minimum(duck[i:i + n], seg[:max(0, min(n, N - i))])
for k in ("pad", "bass", "synth"):
    bus[k] *= duck


def reverb_ir(dur=2.4, decay=3.2):
    n = int(dur * SR); t = np.arange(n) / SR
    ir = np.vstack([noise(n), noise(n)]) * np.exp(-t * decay)
    ir = filt(ir, 5500)
    ir[:, : int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


IR = reverb_ir()
send = bus["pad"] * 0.35 + bus["synth"] * 0.45 + bus["fx"] * 0.5 + bus["drums"] * 0.12
wet = np.vstack([signal.fftconvolve(send[c], IR[c])[:N] for c in range(2)]) * 0.35

mix = (bus["drums"] * 0.95 + bus["bass"] * 0.85 + bus["synth"] * 0.8 + bus["pad"] * 0.75
       + bus["fx"] * 0.9 + wet)
mix = filt(mix, 28, "highpass")
# gentle glue: soft clip with drive normalised
mix = mix / np.max(np.abs(mix)) * 1.6
mix = np.tanh(mix) / np.tanh(1.6)
# fade the final 0.35s
f = int(0.35 * SR)
mix[:, -f:] *= np.linspace(1, 0, f) ** 2
mix *= 0.89
WORK.mkdir(parents=True, exist_ok=True)
sf.write(str(WORK / "music.wav"), mix.T.astype(np.float32), SR, subtype="FLOAT")
# stems for the mix (clip SFX duck against drums would be overkill; kept for inspection)
print("peak", np.max(np.abs(mix)), "rms", np.sqrt(np.mean(mix ** 2)))
