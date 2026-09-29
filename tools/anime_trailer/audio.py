#!/usr/bin/env python3
"""The anime trailer's score and sound, synthesized — no samples, no licences.

  python3 audio.py --cues cues.json --out mix.wav [--stems]

Everything is cut to the picture's grid: 144 bpm, 10 frames a beat at 24 fps.
The SCORE is composed here in beats; the SOUND EFFECTS come from cues.json,
which the picture exports (capture.py --cues), so a hit on screen and its
sound are the same number and cannot drift apart.

D minor. The hook is Dm - Bb - F - C, the anime-opening progression.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
BPM = 144
BEAT = 60 / BPM
TOTAL_BEATS = 102
DUR = TOTAL_BEATS * BEAT
N = int(round(DUR * SR))
TAU = 2 * np.pi


# ------------------------------------------------------------------ basics
def mtof(m): return 440.0 * 2 ** ((np.asarray(m, dtype=float) - 69) / 12)
def tt(d): return np.arange(max(1, int(round(d * SR)))) / SR
def rng(seed): return np.random.default_rng(seed)
def noise(d, seed=0): return rng(seed).uniform(-1, 1, max(1, int(round(d * SR))))


def sos(kind, fc, order=2, q=None):
    if kind == "band":
        lo, hi = fc
        lo = max(20, lo); hi = max(lo * 1.2, min(SR * 0.45, hi))
        return signal.butter(order, [max(20, lo), min(SR * 0.45, hi)], "band", fs=SR, output="sos")
    return signal.butter(order, min(max(20, fc), SR * 0.45), kind, fs=SR, output="sos")


def lp(x, fc, o=2): return signal.sosfilt(sos("low", fc, o), x)
def hp(x, fc, o=2): return signal.sosfilt(sos("high", fc, o), x)
def bp(x, lo, hi, o=2): return signal.sosfilt(sos("band", (lo, hi), o), x)


def sweep(x, fcs, kind="low", block=256, o=2):
    """Time-varying filter: coefficients per block, state carried across."""
    y = np.zeros_like(x)
    zi = None
    for i in range(0, len(x), block):
        fc = max(60.0, float(np.mean(fcs[i:i + block])))
        if kind == "band":
            s = sos("band", (fc * 0.7, fc * 1.4), o)
        else:
            s = sos(kind, fc, o)
        if zi is None or zi.shape != (s.shape[0], 2):
            zi = np.zeros((s.shape[0], 2))
        y[i:i + block], zi = signal.sosfilt(s, x[i:i + block], zi=zi)
    return y


def saw(freq):
    """PolyBLEP sawtooth; `freq` is a per-sample array."""
    dt = np.clip(freq / SR, 1e-6, 0.49)
    ph = np.cumsum(dt) % 1.0
    s = 2 * ph - 1
    m = ph < dt
    u = ph[m] / dt[m]; s[m] -= u + u - u * u - 1
    m = ph > 1 - dt
    u = (ph[m] - 1) / dt[m]; s[m] -= u * u + u + u + 1
    return s


def sine(freq, ph0=0.0): return np.sin(ph0 + TAU * np.cumsum(np.broadcast_to(freq, freq.shape) / SR))


def env(d, a=0.005, dcy=0.1, s=0.7, r=0.1, curve=4.0):
    n = max(1, int(round(d * SR)))
    t = np.arange(n) / SR
    e = np.ones(n) * s
    e[t < a] = t[t < a] / max(a, 1e-6)
    m = (t >= a) & (t < a + dcy)
    e[m] = 1 - (1 - s) * (1 - np.exp(-curve * (t[m] - a) / max(dcy, 1e-6))) / (1 - np.exp(-curve))
    rel = t > d - r
    e[rel] *= np.clip((d - t[rel]) / max(r, 1e-6), 0, 1)
    return e


def edec(d, tau): return np.exp(-tt(d) / tau)


def pan2(x, p=0.0):
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1)


class Bus:
    def __init__(self): self.b = np.zeros((N, 2))

    def add(self, x, t, g=1.0, p=0.0):
        if x.ndim == 1:
            x = pan2(x, p)
        i = int(round(t * SR))
        if i >= N:
            return
        if i < 0:
            x = x[-i:]; i = 0
        n = min(len(x), N - i)
        self.b[i:i + n] += x[:n] * g


def reverb_ir(rt, seed, bright=7000, pre=0.012):
    n = int(rt * 1.3 * SR)
    t = np.arange(n) / SR
    L = []
    for ch in range(2):
        x = rng(seed + ch).standard_normal(n) * np.exp(-6.9 * t / rt)
        x = lp(x, bright, 1)
        x[: int(pre * SR)] = 0
        L.append(x)
    ir = np.stack(L, 1)
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    out = np.zeros_like(x)
    for ch in range(2):
        out[:, ch] = signal.fftconvolve(x[:, ch], ir[:, ch])[: len(x)]
    return out


def B(beat): return beat * BEAT


# ------------------------------------------------------------------ instruments
def supersaw(midis, d, detune=0.16, voices=7, seed=1, vib=0.0):
    t = tt(d)
    out = np.zeros(len(t))
    r = rng(seed)
    for m in np.atleast_1d(midis):
        f0 = mtof(m)
        for v in range(voices):
            cents = (v - (voices - 1) / 2) / ((voices - 1) / 2) * detune * 100
            f = f0 * 2 ** (cents / 1200) * (1 + vib * 0.006 * np.sin(TAU * 5.2 * t + r.uniform(0, 6)))
            out += np.roll(saw(np.full(len(t), f) if np.isscalar(f) or np.ndim(f) == 0 else f), r.integers(0, 2000))
    return out / np.sqrt(voices * len(np.atleast_1d(midis)))


def brass_stab(midis, d=0.7, bright=5200, seed=3):
    x = supersaw(midis, d, 0.12, 5, seed)
    fc = 700 + (bright - 700) * np.exp(-tt(d) / 0.12)
    x = sweep(x, fc, "low")
    x = np.tanh(2.2 * x) * env(d, 0.004, 0.25, 0.35, 0.2)
    return x


def pad(midis, d, a=0.4, r=0.6, fc=1800, seed=5):
    x = supersaw(midis, d, 0.2, 7, seed, vib=1.0)
    return lp(x, fc, 2) * env(d, a, 0.5, 0.85, r)


def choir(midis, d, a=0.5, r=0.8, seed=9):
    t = tt(d)
    src = np.zeros(len(t))
    r_ = rng(seed)
    for m in np.atleast_1d(midis):
        for v in range(4):
            f = mtof(m) * (1 + 0.004 * (v - 1.5)) * (1 + 0.005 * np.sin(TAU * (5 + 0.3 * v) * t + r_.uniform(0, 6)))
            src += saw(f)
    y = bp(src, 650, 820, 2) * 1.0 + bp(src, 1000, 1200, 2) * 0.6 + bp(src, 2300, 2700, 2) * 0.25
    return y / (2.2 * np.sqrt(len(np.atleast_1d(midis)))) * env(d, a, 0.6, 0.9, r)


def pluck(m, d, bright=3000, seed=0):
    f = mtof(m)
    x = saw(np.full(int(d * SR), f)) * 0.6 + 0.4 * np.sign(np.sin(TAU * f * tt(d)))
    fc = 400 + bright * np.exp(-tt(d) / 0.08)
    return sweep(x, fc) * env(d, 0.002, 0.12, 0.25, 0.06)


def bass(m, d):
    f = mtof(m)
    x = saw(np.full(int(d * SR), f)) * 0.7 + np.sin(TAU * f / 2 * tt(d)) * 0.8
    x = lp(x, 900, 2)
    return np.tanh(1.8 * x) * env(d, 0.003, 0.1, 0.8, 0.04)


def lead(m, d):
    t = tt(d)
    f = mtof(m) * (1 + 0.012 * np.sin(TAU * 5.5 * t) * np.clip((t - 0.12) / 0.2, 0, 1))
    x = saw(f) * 0.5 + saw(f * 1.004) * 0.5 + 0.35 * np.sign(np.sin(TAU * np.cumsum(f) / SR * 2 * np.pi / TAU))
    x = lp(x, 3800, 2)
    return x * env(d, 0.01, 0.2, 0.75, 0.05) * 0.8


def bell(m, d=1.6):
    f = mtof(m)
    t = tt(d)
    x = np.zeros(len(t))
    for k, (ratio, amp, tau) in enumerate([(1, 1, 1.2), (2.0, 0.5, 0.6), (3.01, 0.35, 0.4), (4.17, 0.25, 0.25), (5.43, 0.2, 0.15)]):
        x += amp * np.sin(TAU * f * ratio * t) * np.exp(-t / tau)
    return x * 0.5 * np.clip(t / 0.002, 0, 1)


def strings_note(m, d):
    t = tt(d)
    f = mtof(m) * (1 + 0.003 * np.sin(TAU * 6 * t))
    x = saw(f) + saw(f * 1.003)
    return lp(x, 2600, 2) * env(d, 0.004, 0.06, 0.6, 0.03) * 0.5


# ------------------------------------------------------------------ drums
def kick(g=1.0):
    d = 0.5; t = tt(d)
    f = 44 + 120 * np.exp(-t * 28)
    x = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = hp(noise(0.006, 11), 2000) * 0.6
    x[: len(click)] += click
    return np.tanh(1.6 * x) * g


def snare(g=1.0, seed=21):
    d = 0.32; t = tt(d)
    body = np.sin(TAU * 190 * t) * np.exp(-t * 24) * 0.7
    nz = bp(noise(d, seed), 1500, 9000) * np.exp(-t * 13)
    return np.tanh(1.4 * (body + nz * 1.3)) * g


def clap(g=1.0, seed=22):
    d = 0.4; t = tt(d)
    e = np.zeros(len(t))
    for k, off in enumerate([0, 0.011, 0.023]):
        i = int(off * SR); e[i:] += np.exp(-(t[: len(t) - i]) * (60 if k < 2 else 11))
    return bp(noise(d, seed), 900, 6000) * e * 0.9 * g


def hat(open_=False, g=1.0, seed=23):
    d = 0.3 if open_ else 0.06
    return hp(noise(d, seed), 7500, 2) * edec(d, 0.09 if open_ else 0.015) * g


def taiko(g=1.0, f0=72, seed=24):
    d = 1.4; t = tt(d)
    f = f0 * 0.75 + f0 * 0.5 * np.exp(-t * 12)
    x = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    slap = lp(noise(0.05, seed), 1200) * np.exp(-tt(0.05) * 60)
    x[: len(slap)] += slap * 0.8
    return np.tanh(1.3 * x) * g


def tom(m, g=1.0):
    d = 0.5; t = tt(d); f0 = mtof(m)
    f = f0 * (1 + 0.6 * np.exp(-t * 20))
    return np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t * 7) * g


def crash(g=1.0, d=2.4, seed=25):
    t = tt(d)
    x = hp(noise(d, seed), 3500, 2) * np.exp(-t / 0.7)
    ring = sum(np.sin(TAU * f * t + i) * np.exp(-t / 0.9) for i, f in enumerate([3120, 4480, 5710, 7390])) * 0.05
    return (x + ring) * g


def sub_drop(d=1.2, f0=90, f1=28, g=1.0):
    t = tt(d)
    f = f1 + (f0 - f1) * np.exp(-t * 3.5)
    return np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t * 2.2) * np.clip(t / 0.004, 0, 1) * g


def braam(midis=(26, 33, 38), d=2.4, g=1.0):
    x = supersaw(midis, d, 0.25, 7, 31)
    fc = 250 + 2600 * np.exp(-tt(d) / 0.5)
    x = sweep(x, fc)
    return np.tanh(2.8 * x) * env(d, 0.02, 0.4, 0.6, 0.8) * g


def rev_crash(d, g=1.0):
    r = crash(1.0, d + 0.1, 77)[::-1]
    return r[-int(d * SR):] * g


def riser(d, g=1.0, seed=41):
    t = tt(d); u = t / d
    nz = sweep(noise(d, seed), 300 + 9000 * u ** 2, "band")
    tone = saw(110 * 2 ** (u * 3)) * 0.25
    return (nz + lp(tone, 4000)) * u ** 2.2 * g


def whoosh(d, g=1.0, up=True, seed=51):
    t = tt(d); u = t / d
    fc = (400 + 5000 * u ** 1.5) if up else (5500 - 5000 * u ** 0.7)
    x = sweep(noise(d, seed), fc, "band")
    e = np.sin(np.pi * np.clip(u, 0, 1)) ** 1.4
    return x * e * 1.6 * g


# ------------------------------------------------------------------ sound effects
def clang(f0=520, d=1.6, g=1.0, seed=61):
    t = tt(d)
    x = sum(a * np.sin(TAU * f0 * r * t + i) * np.exp(-t / tau)
            for i, (r, a, tau) in enumerate([(1, 1, 0.6), (2.76, 0.6, 0.35), (5.4, 0.45, 0.22), (8.93, 0.3, 0.12), (13.3, 0.2, 0.06)]))
    hit = hp(noise(0.03, seed), 1500) * np.exp(-tt(0.03) * 90)
    x[: len(hit)] += hit * 1.5
    return x * 0.45 * g


def impact(g=1.0, size=1.0, seed=62):
    d = 1.4 * size
    x = sub_drop(d, 110, 30) * 1.2
    nz = lp(noise(d, seed), 2500 / size) * np.exp(-tt(d) * 6 / size)
    x = x + nz * 0.9
    k = kick(1.0)
    n = min(len(k), len(x))
    x[:n] += k[:n]
    return np.tanh(1.5 * x) * g


def explosion(g=1.0, d=2.2, seed=63):
    t = tt(d)
    body = lp(noise(d, seed), 900, 2) * np.exp(-t * 2.2) * 2.0
    crack = hp(noise(d, seed + 1), 1200) * np.exp(-t * 9) * 0.7
    crackle = hp(noise(d, seed + 2), 2500) * (rng(seed).random(len(t)) > 0.985) * np.exp(-t * 1.5) * 1.2
    return np.tanh(1.2 * (body + crack + crackle + sub_drop(d, 80, 25) * 1.2)) * g


def glass_shatter(g=1.0, seed=64):
    d = 1.2
    out = hp(noise(d, seed), 3000) * np.exp(-tt(d) * 7) * 0.6
    r = rng(seed)
    for k in range(70):
        st = r.uniform(0, 0.55) ** 1.6
        f = r.uniform(2400, 9000)
        dd = r.uniform(0.05, 0.3)
        i = int(st * SR)
        p = np.sin(TAU * f * tt(dd)) * np.exp(-tt(dd) / (dd / 4)) * r.uniform(0.1, 0.35)
        out[i:i + len(p)] += p[: len(out) - i]
    return out * g


def crack_sfx(g=1.0, seed=65):
    d = 0.35
    x = hp(noise(d, seed), 1800) * np.exp(-tt(d) * 30)
    for f in (3300, 4700, 6100):
        x += np.sin(TAU * f * tt(d)) * np.exp(-tt(d) * 18) * 0.2
    return x * g


def zap(d, g=1.0, seed=66):
    t = tt(d); r = rng(seed)
    gate = np.repeat(r.random(int(d * 200) + 1) > 0.45, SR // 200 + 1)[: len(t)]
    buzz = np.sign(np.sin(TAU * (120 + 60 * r.random()) * t)) * 0.3
    x = (hp(noise(d, seed), 2500) * 0.8 + buzz) * gate * np.clip(1 - t / d, 0, 1)
    return lp(x, 9000) * g


def fire_roar(d=1.0, g=1.0, seed=67):
    t = tt(d)
    x = lp(noise(d, seed), 1800, 2) * 1.6 + bp(noise(d, seed + 1), 200, 600) * 1.2
    crackle = hp(noise(d, seed + 2), 3000) * (rng(seed).random(len(t)) > 0.99) * 1.5
    e = np.clip(t / 0.03, 0, 1) * np.exp(-np.clip(t - 0.35, 0, None) * 4)
    return np.tanh((x + crackle) * e) * g


def beam(d, g=1.0):
    t = tt(d)
    body = supersaw((50, 57, 62, 69), d, 0.3, 5, 71)
    wob = 1400 + 900 * np.sin(TAU * 7 * t)
    x = sweep(body, wob) * 0.9 + bp(noise(d, 72), 800, 3000) * 0.5 + sub_drop(d, 60, 45) * 0.6
    e = np.clip(t / 0.02, 0, 1) * np.clip((d - t) / 0.5, 0, 1)
    return np.tanh(1.8 * x) * e * g


def charge_up(d, g=1.0):
    t = tt(d); u = t / d
    f = 110 * 2 ** (u * 3.2)
    trem = 0.6 + 0.4 * np.sin(TAU * np.cumsum(4 + 26 * u) / SR)
    x = (saw(f) * 0.5 + np.sin(TAU * np.cumsum(f * 2) / SR) * 0.5) * trem
    sh = hp(noise(d, 73), 6000) * 0.3 * u
    return (lp(x, 1200 + 6000 * u.mean()) + sh) * u ** 1.3 * g


def tornado(d, g=1.0):
    t = tt(d)
    c = 600 + 400 * np.sin(TAU * 0.9 * t) + 250 * np.sin(TAU * 2.3 * t)
    x = sweep(noise(d, 74), c, "band") * 2.2 + lp(noise(d, 75), 250) * 1.5
    e = np.clip(t / 0.4, 0, 1) * np.clip((d - t) / 0.3, 0, 1)
    L = x * (0.6 + 0.4 * np.sin(TAU * 1.3 * t)); R = x * (0.6 - 0.4 * np.sin(TAU * 1.3 * t))
    return np.stack([L, R], 1) * e[:, None] * g


def blip(f=1300, d=0.09, g=1.0):
    t = tt(d)
    return np.sin(TAU * f * t + 3 * np.sin(TAU * f * 1.5 * t) * np.exp(-t * 40)) * np.exp(-t * 45) * g


def ping(f, d=0.5, g=1.0):
    t = tt(d)
    return (np.sin(TAU * f * t) + 0.4 * np.sin(TAU * f * 2.7 * t)) * np.exp(-t * 9) * np.clip(t / 0.001, 0, 1) * g


def shing(g=1.0, seed=76):
    d = 0.5; t = tt(d)
    x = bp(noise(d, seed), 4000, 11000) * np.exp(-t * 9)
    x += np.sin(TAU * 6200 * t) * np.exp(-t * 7) * 0.25 + np.sin(TAU * 8300 * t) * np.exp(-t * 10) * 0.15
    return x * g


def spin_up(d, g=1.0):
    t = tt(d); u = t / d
    rate = 2 + 22 * u ** 1.5
    am = 0.5 + 0.5 * np.sin(TAU * np.cumsum(rate) / SR)
    x = bp(noise(d, 77), 300, 1800) * am * (0.4 + 0.6 * u)
    return x * g


def ghost(d, g=1.0):
    t = tt(d); u = t / d
    x = choir((50, 57, 62), d, 0.2, 0.3) * 0.8
    w = sweep(noise(d, 78), 300 + 2000 * u, "band") * 0.8
    return (x + w) * u * g


def wire(g=1.0):
    d = 0.9
    x = clang(1450, d, 1.0, 79) * 0.6 + bp(noise(d, 80), 2500, 7000) * np.exp(-tt(d) * 6) * 0.5
    return x * g


def rustle(d, g=1.0):
    t = tt(d); r = rng(81)
    am = np.repeat(r.random(int(d * 60) + 2), SR // 60 + 1)[: len(t)]
    return bp(noise(d, 82), 2000, 7000) * am * g


def whistle(f0=3000, d=0.35, g=1.0):
    t = tt(d)
    f = f0 * (1 - 0.45 * t / d)
    return (np.sin(TAU * np.cumsum(f) / SR) * 0.5 + bp(noise(d, 83), 2000, 6000) * 0.4) * np.sin(np.pi * t / d) * g


def thud(g=1.0):
    d = 0.6
    return np.tanh(2 * (sub_drop(d, 120, 40) + lp(noise(d, 84), 600) * np.exp(-tt(d) * 14))) * g


# ------------------------------------------------------------------ the score
DM, BB, FM, CM, AM = (50, 53, 57), (46, 50, 53), (53, 57, 60), (48, 52, 55), (45, 49, 52)
PROG = [("Dm", DM, 38), ("Bb", BB, 34), ("F", FM, 41), ("C", CM, 36)]
HOOK = [  # (beat within 4 bars, dur beats, midi)
    (0, .5, 69), (.5, .5, 74), (1, .5, 76), (1.5, 1, 77), (2.5, .5, 76), (3, 1, 74),
    (4, .5, 74), (4.5, .5, 77), (5, .5, 79), (5.5, 1.5, 81), (7, .5, 79), (7.5, .5, 77),
    (8, .5, 77), (8.5, .5, 81), (9, 1, 84), (10, .5, 81), (10.5, .5, 79), (11, 1, 77),
    (12, 1, 76), (13, 1, 79), (14, .5, 76), (14.5, .5, 74), (15, .5, 72), (15.5, .5, 76),
]


def in_any(b, spans): return any(a <= b < c for a, c in spans)


def score(mus: Bus, drum: Bus):
    GROOVE = [(16, 41), (42.5, 62.2), (63.5, 74)]
    DRUMS_OFF = [(41, 42.5), (62.2, 63.5)]
    FILLS = [(35, 36), (47, 48), (59, 60), (65, 66), (73, 74)]

    # --- A: cold open (0-8)
    mus.add(riser(B(1), 0.5), 0)
    drum.add(rev_crash(B(1), 0.5), 0)
    mus.add(brass_stab(DM + (62,), 1.2), B(1), 0.9)
    drum.add(taiko(1.2), B(1)); drum.add(crash(0.7), B(1)); drum.add(kick(1.0), B(1))
    drone = pad((26, 38, 45), B(7), 0.3, 0.8, 500)
    mus.add(drone, B(1), 0.55)
    for k in range(int(3 * 8)):                                 # tremolo strings: tension
        mus.add(strings_note(74 if k % 8 < 6 else 75, B(0.125)), B(1 + k * 0.125), 0.12 + 0.12 * k / 24, 0.2)
    for b in (2, 3):
        drum.add(taiko(0.7), B(b))
    for k in range(24):
        drum.add(hat(False, 0.12), B(1 + k * 0.125), p=0.3)
    mus.add(brass_stab(BB + (58,), 1.0), B(4), 0.8)
    drum.add(taiko(1.1), B(4)); drum.add(crash(0.5), B(4))
    mus.add(braam((26, 33, 38), B(2.5), 0.9), B(5.5))
    drum.add(taiko(0.9), B(5.5))
    drum.add(rev_crash(B(1.0), 0.8), B(7))

    # --- B: the crown (8-16)
    mus.add(choir((62, 65, 69), B(3.2), 0.6, 0.5), B(8), 0.6)
    for i, (b, m) in enumerate([(8, 86), (8.5, 81), (9, 77), (9.5, 76), (10, 74), (10.5, 72), (10.75, 69)]):
        mus.add(bell(m, 1.4), B(b), 0.35, p=(-0.4 if i % 2 else 0.4))
    mus.add(brass_stab(DM + (62, 65), 1.4), B(11), 1.0)
    mus.add(braam((26, 38), B(2), 0.7), B(11))
    drum.add(taiko(1.3), B(11)); drum.add(crash(0.9), B(11))
    mus.add(choir((62, 65, 69, 74), B(5), 0.3, 0.3), B(11), 0.7)
    for k in range(8):                                           # low string pulse
        mus.add(strings_note(38, B(0.45)), B(12 + k * 0.5), 0.5)
    for k in range(32):                                          # taiko crescendo
        b = 13 + k * (3 / 32)
        drum.add(taiko(0.25 + 0.55 * k / 31, 90 if k % 2 else 75), B(b), p=(-0.3 if k % 2 else 0.3))
    for k in range(16):
        drum.add(snare(0.15 + 0.5 * k / 15), B(15 + k / 16))
    mus.add(riser(B(2), 0.6), B(14))

    # --- the groove: C (16-24), D (24-66), E (66-74)
    CH = {"Dm": (DM, 38), "Bb": (BB, 34), "F": (FM, 41), "C": (CM, 36), "A": (AM, 33)}
    BARS = {16: "Dm", 20: "C", 24: "Dm", 28: "Bb", 32: "F", 36: "C", 40: "Dm", 44: "A",
            48: "Dm", 52: "Bb", 56: "F", 60: "C", 64: "Dm", 68: "Bb", 72: "C"}
    for bar in range(16, 74, 4):
        chord, root = CH[BARS[bar]]
        for q in range(8):                                       # bass 8ths, octave jumps
            b = bar + q * 0.5
            if in_any(b, DRUMS_OFF) or not in_any(b, GROOVE):
                continue
            mus.add(bass(root + (12 if q % 4 == 3 else 0), B(0.45)), B(b), 0.55)
        for q in range(16):                                      # strings ostinato 16ths
            b = bar + q * 0.25
            if in_any(b, DRUMS_OFF) or not in_any(b, GROOVE):
                continue
            tones = [chord[0] + 12, chord[2] + 12, chord[0] + 24, chord[2] + 12]
            mus.add(strings_note(tones[q % 4], B(0.22)), B(b), 0.22, p=(-0.35 if q % 2 else 0.35))
        if in_any(bar, GROOVE) and not in_any(bar, DRUMS_OFF):
            mus.add(pad(tuple(c + 12 for c in chord), B(4), 0.05, 0.3, 2200), B(bar), 0.22)
    for b16 in np.arange(16, 74, 0.25):                          # drums
        b = float(b16)
        if not in_any(b, GROOVE) or in_any(b, DRUMS_OFF):
            continue
        pos = (b - 16) % 4
        fill = in_any(b, FILLS)
        four = b < 24 or b >= 66
        if fill:
            k = (b - int(b)) * 4
            drum.add(snare(0.35 + 0.6 * ((b % 1) + (1 if b % 2 >= 1 else 0)) / 2), B(b))
            if pos == 0:
                drum.add(kick(1.0), B(b))
            continue
        if (four and pos % 1 == 0) or (not four and pos in (0, 1.5, 2, 2.75)):
            drum.add(kick(0.95), B(b))
        if pos in (1, 3):
            drum.add(snare(0.8), B(b)); drum.add(clap(0.35), B(b))
        if pos % 0.5 == 0:
            drum.add(hat(pos == 3.5, 0.22 if pos % 1 else 0.14), B(b), p=0.25)
        elif b >= 66:
            drum.add(hat(False, 0.1), B(b), p=-0.25)
    for b in (16, 24, 36, 42.5, 48, 60, 63.5, 66, 70):
        drum.add(crash(0.55), B(b), p=(-0.3 if int(b) % 2 else 0.3))
    for base in (24, 48):                                        # the hook
        for (o, d, m) in HOOK:
            b = base + o
            if in_any(b, DRUMS_OFF) or (base == 48 and b >= 62):
                continue
            mus.add(lead(m, B(d) * 0.95), B(b), 0.3)
            mus.add(lead(m + 12, B(d) * 0.95), B(b), 0.08)
    for (o, d, m) in HOOK[:12]:                                  # after the garrote: the hook, up an octave
        if o < 8:
            mus.add(lead(m + 12, B(d) * 0.95), B(64 + o), 0.2)
    for i, b in enumerate(range(16, 24)):                        # the seven: a stab each
        ch = [DM, DM, BB, BB, CM, CM, AM, DM][i]
        mus.add(brass_stab(tuple(c + 12 for c in ch), 0.5), B(b), 0.55)
    for i, b in enumerate(range(66, 74)):
        ch = [DM, BB, FM, CM, DM, BB, CM, AM][i]
        mus.add(brass_stab(tuple(c + 12 for c in ch), 0.45), B(b), 0.5)
    # the cut-ins and callouts: a stab and a taiko on the downbeat
    for b in (27, 36.6, 41.05, 50, 60.3):
        mus.add(brass_stab(DM + (62, 65), 1.0), B(b), 0.7)
        drum.add(taiko(1.0), B(b))
    # the Sentinel's charge: drums out, strings tremolo up, riser
    for k in range(12):
        mus.add(strings_note(74 + (k // 4) * 3, B(0.125)), B(41 + k * 0.125), 0.2 + 0.03 * k)
    # the garrote's wind: drone and ticking
    mus.add(pad((38, 45, 50), B(1.3), 0.05, 0.1, 700), B(62.2), 0.5)
    for k in range(10):
        drum.add(hat(False, 0.3), B(62.2 + k * 0.13))

    # --- F: the rematch (74-86)
    mus.add(brass_stab(DM + (62, 65), 1.4), B(74), 1.0)
    drum.add(taiko(1.3), B(74)); drum.add(crash(0.9), B(74))
    mus.add(choir((62, 65, 69), B(4), 0.2, 0.3), B(74), 0.55)
    mus.add(pad((26, 38), B(4), 0.05, 0.3, 400), B(74), 0.5)
    for b in (74, 76):
        drum.add(kick(1.0), B(b)); drum.add(taiko(0.9), B(b))
    for b in (75, 77):
        drum.add(snare(0.9), B(b)); drum.add(clap(0.6), B(b))
    mus.add(brass_stab(BB + (58,), 1.0), B(76), 0.7)
    # the build
    k = 0
    for b in np.arange(78, 81, 0.125):
        step = 0.5 if b < 79 else (0.25 if b < 80 else 0.125)
        if (b - 78) % step < 1e-6:
            drum.add(snare(0.25 + 0.7 * (b - 78) / 3), B(b), p=(0.2 if k % 2 else -0.2)); k += 1
    for b in (78, 79, 80):
        drum.add(kick(1.0), B(b)); drum.add(tom(45 + 5 * (b - 78), 0.8), B(b))
    for j in range(24):
        mus.add(strings_note(62 + j, B(0.125)), B(78 + j * 0.125), 0.25)
    mus.add(riser(B(3), 0.8), B(78))
    # 81: silence — nothing is scheduled between 81 and 81.5
    mus.add(bell(98, 0.8), B(81), 0.15)
    # 81.5: the clash
    mus.add(brass_stab(DM + (62, 65, 74), 2.0), B(81.5), 1.1)
    mus.add(braam((26, 33, 38, 45), B(4), 1.0), B(81.5))
    drum.add(taiko(1.4), B(81.5)); drum.add(taiko(1.2, 60), B(81.5)); drum.add(crash(1.0, 3.2), B(81.5)); drum.add(crash(0.7, 3.2, 99), B(81.5), p=0.5)
    mus.add(choir((62, 65, 69, 74), B(4.5), 1.0, 0.4), B(81.5), 0.6)
    mus.add(riser(B(2.5), 0.4), B(83.5))

    # --- G: the crown (86-102)
    mus.add(pad((50, 57, 62, 65), B(4), 0.3, 0.6, 1200), B(86), 0.4)
    for k, m in enumerate([74, 77, 79, 81, 84, 86, 89]):
        mus.add(bell(m, 1.6), B(87 + k * 0.28), 0.45, p=(-0.5 + k / 6))
    mus.add(brass_stab(BB + (58, 62), 1.3), B(89.5), 0.8)
    drum.add(taiko(1.1), B(89.5)); drum.add(crash(0.7), B(89.5))
    for i, (b, ch, root) in enumerate([(90, DM, 26), (92, BB, 22), (94, FM, 29), (96, CM, 24), (98, DM, 26)]):
        d = 2 if b < 98 else 4
        mus.add(choir(tuple(c + 12 for c in ch), B(d) + 0.2, 0.08, 0.4), B(b), 0.7)
        mus.add(pad(tuple(c for c in ch) + (root + 12,), B(d) + 0.2, 0.05, 0.5, 1600), B(b), 0.45)
        mus.add(bass(root + 12, B(d) * 0.98), B(b), 0.5)
        mus.add(brass_stab(tuple(c + 12 for c in ch), 1.2, 3500), B(b), 0.6)
        drum.add(taiko(1.1 if i == 0 else 0.8), B(b)); drum.add(kick(0.9), B(b))
        if b < 98:
            drum.add(snare(0.6), B(b + 1)); drum.add(clap(0.4), B(b + 1))
            for q in range(4):
                drum.add(hat(False, 0.12), B(b + q * 0.5), p=0.25)
    mus.add(braam((26, 38), B(3), 0.7), B(90))
    drum.add(crash(0.9), B(90))
    for b in (90, 90.25):
        drum.add(taiko(1.0, 64), B(b))
    for (b, d, m) in [(90, 1, 74), (91, 1, 81), (92, 1.5, 82), (93.5, .5, 81), (94, 1, 77), (95, 1, 81), (96, 2, 79), (98, 3.5, 74)]:
        mus.add(lead(m, B(d) * 0.95), B(b), 0.22)                # the fanfare, on chord tones
        mus.add(brass_stab((m - 12, m), B(d) * 0.95, 3000), B(b), 0.3)
    mus.add(bell(86, 3.0), B(98), 0.4)
    mus.add(bell(74, 3.0), B(98), 0.3)


# ------------------------------------------------------------------ the effects
def effects(fx: Bus, cues):
    for c in cues:
        k, t = c["kind"], c["t"]
        d = c.get("dur", 0.5)
        if k == "whoosh_in": fx.add(whoosh(d, 0.9), t)
        elif k == "clash_big":
            fx.add(clang(520, 1.8, 1.0), t, p=-0.2); fx.add(clang(610, 1.8, 0.8, 91), t, p=0.2)
            fx.add(impact(1.0), t); fx.add(explosion(0.5, 1.5), t)
        elif k == "grind":
            t_ = tt(d); x = bp(noise(d, 92), 1800, 5200) * (0.5 + 0.5 * np.abs(np.sin(TAU * 11 * t_))) * np.exp(-t_ * 0.8)
            x += sum(np.sin(TAU * f * t_) * 0.06 for f in (2210, 3170, 4410))
            fx.add(x * 0.6, t)
        elif k == "taiko_hit": pass
        elif k == "hit_big": fx.add(impact(0.9), t); fx.add(shing(0.5), t)
        elif k == "hit_huge": fx.add(impact(1.1, 1.3), t); fx.add(clang(380, 1.2, 0.5), t)
        elif k == "wallslam": fx.add(thud(1.0), t); fx.add(explosion(0.4, 1.0, 93), t)
        elif k == "slam_text": fx.add(kick(0.7), t); fx.add(hp(noise(0.25, 94), 3000) * edec(0.25, 0.05) * 0.5, t)
        elif k == "slam_soft": fx.add(kick(0.4), t)
        elif k == "reverse_whoosh": fx.add(whoosh(d, 0.8)[::-1], t)
        elif k == "crown_hum":
            t_ = tt(d); fx.add(sum(np.sin(TAU * f * t_) * 0.05 * (1 + np.sin(TAU * 3 * t_ + f)) for f in (1175, 1480, 1760, 2350)) * np.clip(t_ / 0.4, 0, 1), t)
        elif k == "crack": fx.add(crack_sfx(0.9, int(t * 100)), t)
        elif k == "shatter": fx.add(glass_shatter(1.0), t); fx.add(impact(0.9), t)
        elif k == "whoosh_out": fx.add(whoosh(d + 0.15, 0.8, seed=int(t * 10)), t)
        elif k == "panel_hit": fx.add(shing(0.55, 100 + c["k"]), t); fx.add(whoosh(0.18, 0.5, seed=110 + c["k"]), t - 0.12)
        elif k == "montage_hit": fx.add(shing(0.45, 120 + c["k"]), t); fx.add(thud(0.4), t)
        elif k == "bow_draw":
            t_ = tt(d); fx.add(bp(noise(d, 95), 300, 1400) * (t_ / d) * 0.4 + np.sin(TAU * (90 + 60 * t_ / d) * t_) * 0.15, t)
        elif k == "crossweave": fx.add(clang(260, 0.6, 0.4), t); fx.add(whoosh(0.4, 0.6, False), t)
        elif k == "zap": fx.add(zap(d, 0.5), t, p=0.2)
        elif k == "dodge": fx.add(whoosh(0.3, 0.9, seed=96), t - 0.1)
        elif k == "cutin": fx.add(shing(0.8), t); fx.add(whoosh(0.25, 0.6), t - 0.2)
        elif k == "callout": fx.add(impact(0.5), t); fx.add(bell(93, 0.8) * 0.3, t)
        elif k == "leaves": fx.add(rustle(d + 0.3, 0.5), t)
        elif k == "kunai_fan":
            for i in range(14):
                fx.add(whistle(2600 + 90 * i, 0.3, 0.2), t + i * 0.012, p=(-0.6 if i < 7 else 0.6))
        elif k == "ricochet":
            n = c.get("n", 1)
            fx.add(ping(1500 * 1.09 ** n, 0.35, 0.18 + 0.03 * n), t, p=float(np.sin(t * 17)) * 0.6)
        elif k == "kunai_hit": fx.add(thud(0.6), t); fx.add(crack_sfx(0.6, 97), t)
        elif k == "scythe_swing": fx.add(whoosh(0.2, 0.8, seed=98), t - 0.05)
        elif k == "wall_tear":
            s = c.get("size", 1.0)
            fx.add(crack_sfx(1.0, 99), t); fx.add(thud(0.8 * s), t); fx.add(fire_roar(0.5, 0.35 * s, 100), t)
        elif k == "heat_jet": fx.add(fire_roar(1.0, 0.7 * c.get("size", 1.0), int(t * 10)), t, p=float(np.sin(t * 3)) * 0.5)
        elif k == "charge": fx.add(charge_up(d, 0.8), t)
        elif k == "beam_fire": fx.add(beam(d, 0.75), t); fx.add(impact(0.9, 1.2), t)
        elif k == "explosion": fx.add(explosion(1.0), t)
        elif k == "shell_lob": fx.add(thud(0.5), t); fx.add(whistle(1800, 0.5, 0.12), t + 0.1)
        elif k == "shell_burst": fx.add(explosion(0.45, 0.8, int(t * 10)), t)
        elif k == "pop": fx.add(blip(700, 0.12, 0.4), t); fx.add(crack_sfx(0.3, int(t * 10)), t)
        elif k == "tornado": fx.add(tornado(d, 0.8), t); fx.add(zap(d, 0.18, 101), t)
        elif k == "tick": fx.add(blip(1250 + 60 * (c.get("k", 0) % 3), 0.08, 0.35), t)
        elif k == "spin_up": fx.add(spin_up(d, 0.8), t)
        elif k == "wire_ring": fx.add(wire(0.7), t)
        elif k == "grasp_reach": fx.add(ghost(d, 0.6), t)
        elif k == "snag": fx.add(wire(0.9), t); fx.add(thud(0.7), t)
        elif k == "tension":
            t_ = tt(d); fx.add(bp(noise(d, 102), 500, 1500) * 0.25 * (t_ / d), t)
        elif k == "vs_slam": fx.add(impact(1.0, 1.2), t); fx.add(clang(300, 1.4, 0.4), t)
        elif k == "dash": fx.add(whoosh(0.35, 1.0, seed=int(t * 10)), t - 0.05)
        elif k == "riser": pass
        elif k == "silence": pass
        elif k == "clash_final":
            fx.add(clang(480, 2.2, 1.0), t, p=-0.25); fx.add(clang(570, 2.2, 0.9, 103), t, p=0.25)
            fx.add(impact(1.2, 1.6), t); fx.add(explosion(1.0, 3.2, 104), t)
        elif k == "glass_crack": fx.add(glass_shatter(0.6, 105), t)
        elif k == "white_swell":
            fx.add(rev_crash(d, 0.6), t); t_ = tt(d)
            fx.add(sum(np.sin(TAU * f * t_) for f in (1175, 1760, 2350)) * 0.05 * (t_ / d) ** 2, t)
        elif k == "shard_lock": fx.add(ping(2200 + 180 * c["k"], 0.4, 0.25), t, p=-0.5 + c["k"] / 6); fx.add(thud(0.25), t)
        elif k == "crown_whole": fx.add(impact(0.7), t); fx.add(glass_shatter(0.25, 106)[::-1], t - 1.2)
        elif k == "title_slam": fx.add(impact(0.8, 1.2), t)
        elif k == "glint": fx.add(ping(5200, 0.9, 0.2), t); fx.add(ping(7800, 0.6, 0.1), t + 0.03)
        else:
            print("unhandled cue:", k, file=sys.stderr)


# ------------------------------------------------------------------ mix
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", default="cues.json")
    ap.add_argument("--out", default="mix.wav")
    ap.add_argument("--stems", action="store_true")
    a = ap.parse_args()
    cues = json.loads(pathlib.Path(a.cues).read_text())

    mus, drum, fx = Bus(), Bus(), Bus()
    score(mus, drum)
    effects(fx, cues)

    hall = reverb_ir(2.4, 201, 6500)
    room = reverb_ir(1.3, 202, 8000)
    music = mus.b + 0.35 * convolve(mus.b, hall)
    drums = drum.b + 0.22 * convolve(drum.b, room)
    sfx = fx.b + 0.25 * convolve(fx.b, room)

    # duck the score under the loudest hits so they land
    hits = [c["t"] for c in cues if c["kind"] in ("clash_big", "hit_huge", "clash_final", "hit_big", "vs_slam", "shatter", "explosion")]
    duck = np.ones(N)
    for h in hits:
        i = int(h * SR); n = int(0.45 * SR)
        seg = 1 - 0.45 * np.exp(-np.arange(n) / SR / 0.15)
        duck[i:i + n] = np.minimum(duck[i:i + n], seg[: max(0, min(n, N - i))])
    music *= duck[:, None]

    mix = music * 0.9 + drums * 0.85 + sfx * 0.95
    # TONE FOR A PHONE: the synth score measured ~8 dB heavy below 120 Hz
    # against a pink reference, energy a phone speaker cannot play and the
    # loudness meter barely counts. Rumble out under 30 Hz, a -5 dB shelf
    # under 120, +2 dB of presence where a phone is loudest.
    for ch in range(2):
        y = hp(mix[:, ch], 30, 2)
        y = y - (1 - 10 ** (-5 / 20)) * lp(y, 120, 2)
        y = y + 0.26 * bp(y, 2000, 5500, 2)
        mix[:, ch] = y
    # THE SILENCE (beat 81) IS ABSOLUTE: everything, reverb tails included,
    # cut hard for half a beat — nothing in it but one high bell.
    s0, s1 = int(B(81) * SR), int(B(81.5) * SR)
    g = np.ones(N); f = int(0.008 * SR)
    g[s0:s0 + f] = np.linspace(1, 0, f); g[s0 + f:s1] = 0; g[s1:s1 + 48] = np.linspace(0, 1, 48)
    mix *= g[:, None]
    bl = Bus(); bl.add(bell(98, 0.55) * 0.25, B(81) + 0.02)
    mix += bl.b
    # glue: a slow RMS compressor, then a soft clip
    rms = np.sqrt(signal.sosfilt(sos("low", 8, 1), np.mean(mix ** 2, 1)) + 1e-9)
    thr = np.percentile(rms, 90)
    gain = np.where(rms > thr, (thr / rms) ** (1 - 1 / 2.5), 1.0)
    mix *= gain[:, None]
    mix /= np.max(np.abs(mix)) + 1e-9
    mix = np.tanh(mix * 1.6) / np.tanh(1.6)
    mix *= 10 ** (-1.2 / 20)
    # a 10ms fade at each end
    f = int(0.01 * SR); mix[:f] *= np.linspace(0, 1, f)[:, None]; mix[-f:] *= np.linspace(1, 0, f)[:, None]
    wavfile.write(a.out, SR, mix.astype(np.float32))
    print(f"{a.out}: {N / SR:.3f}s, peak {np.max(np.abs(mix)):.3f}")
    if a.stems:
        for name, x in (("music", music), ("drums", drums), ("sfx", sfx)):
            wavfile.write(f"stem_{name}.wav", SR, (x / (np.max(np.abs(x)) + 1e-9)).astype(np.float32))
    return 0


if __name__ == "__main__":
    sys.exit(main())
