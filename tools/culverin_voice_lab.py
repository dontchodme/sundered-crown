#!/usr/bin/env python
"""CULVERIN'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v96.

    python culverin_voice_lab.py --game ../02-chain/sc-ironfall-blade.html [--json out.json]
    python culverin_voice_lab.py --game ../02-chain/sc-ironfall-fx.html --shipped

Design §6.2, every clause of it:
  the spell   "a deep short thud on leaving (a cannon at a distance) and a
              stone crack on landing -- the heaviest basic-attack voice in the
              game, on purpose (it fires half as often as an arrow)."
  cast        "a mechanical ratchet into a low boom, 0.4s."
  a shell     "the thud pitched down, then a whistle on the way down, then the
              burst (a bass hit with a stone rattle)."
  close       "the ratchet reversed."

Rick, 2026-09-27, for the staff row: "you pick i overrule". So this lab does
not offer a spread: it renders three candidates a voice beside CONTROLS, prints
the numbers each pick is made on, and PICKS by the rule written beside each
voice below (zenith_voice_lab's method, v98). He overrules from one clip.

WHERE EACH ONE FIRES (culverin_build stage 6):
  thud     `loose {spell:"slug"}` from spawnShot, every slug (~100 a fight)
  crack    `slug-land` from tickShots' spent branch, a slug dying on stone
  cast     `ult {w:"culverin"}` -- fireUlt plays it for every relic today and
           Culverin falls through to the shared rune-crack (a control below)
  shell    `ult {w:"culverin-shell"}` from tickIronfall, each shell loosed
  whistle  `ult {w:"culverin-whistle", dur}` from tickIronfall, the step a
           shell's vy turns downward; `dur` = the flight it has left
  burst    `ult {w:"culverin-burst"}` from the shard pop, a shell reaching its
           mark -- the pop was silent (Ironbloom's splinters never had one)
  close    `ult {w:"culverin-close"}` from tickIronfall, the window running
           out by its clock with the caster alive, never on a death

HOW THE NUMBERS ARE MADE (a subset of zenith_voice_lab's, same definitions):
  every render: OfflineAudioContext 48 kHz through `Sfx.buildChain`, the event
  at t = 1.0, on a synth built the way render.py builds one (Object.create of
  the Sfx prototype, xorshift noise). Noise-built voices are rendered on four
  noise draws and judged on the WORST.
  TOP = the loudest 50 ms RMS (dB) and when it is centred; AUDIBLE = first to
  last 5 ms RMS window above 2% of the voice's own loudest; CENTROID = the
  power-weighted mean frequency; LOW = the share of power under 150 Hz (and in
  the first 60 ms: LOW60); REG = cosine similarity of 1/3-octave band
  amplitudes (25 Hz-16 kHz) against a control -- 1.0 is the same register;
  CLICKS = transients in the >1 kHz envelope in the first 300 ms (the ratchet);
  GLIDE = semitones between the pitch in the first and last quarter; HI20 =
  the share of power over 1 kHz in the first 20 ms (does it OPEN bright);
  PHONE = the TOP of the voice high-passed at 200 Hz -- what a phone speaker
  reproduces, because the deliverable is watched on phones.
  vs HIT = TOP minus the TOP of Culverin's own slug blow (the hit at 21.6, a
  blade of 13.5 at 1.6): every voice is placed against the thing it must not
  drown.

EVERY CANDIDATE IS LEVEL-MATCHED to its voice's target before it is judged
(zenith_voice_lab's method), so a pick is made on shape; the gains are rounded
before the render that is measured. The close is the exception: its clicks are
the cast's own at 0.7. The rules took four rounds and every round is saved in
`06-docs/v96/runs/build/stage6_voice_lab_round*.txt`; the build doc §6c says
what each one corrected (the phone band is the one that mattered: the first
thud picked was 57 dB down above 200 Hz, under the bow's own release).

`--shipped` renders the BUILD's own play() for every event and compares it to
the picked body: the arm that ships must sit inside the renderer's OWN floor --
the same body rendered twice in fresh offline contexts differs by up to ~6e-8
once a voice has more than a few nodes, so "bit for bit" is not available and
the floor itself must be under -120 dB.
"""
from __future__ import annotations
import argparse, base64, json, math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
SR = 48000
T0 = 1.0

# ------------------------------------------------------------ CANDIDATES ---
# Each is a JS body over (S, t, p): the synth, the event time, the opts. The
# body that is PICKED is pasted verbatim into Sfx.play by culverin_build, so
# what ships is exactly what was measured.
THUD = {
 "THUMP": """
  S._tone (t, { freq: 96, to: 42, gain: 0.16, dur: 0.16, type:"sine" });
  S._burst(t, { freq: 240, q: 0.7, gain: 0.10, dur: 0.08, type:"lowpass" });""",
 "FARBOOM": """
  S._burst(t, { freq: 420, q: 0.9, gain: 0.05, dur: 0.05, type:"bandpass" });
  S._tone (t, { freq: 72, to: 34, gain: 0.18, dur: 0.22, type:"sine" });
  S._burst(t, { freq: 160, q: 0.6, gain: 0.08, dur: 0.16, type:"lowpass" });""",
 "CHUFF": """
  S._burst(t, { freq: 300, q: 0.8, gain: 0.14, dur: 0.12, type:"lowpass" });
  S._tone (t, { freq: 118, to: 58, gain: 0.10, dur: 0.12, type:"triangle" });""",
}
CRACK = {
 # ROUND 2. Round 1's three (SPLIT, CHIP, GRIT; runs/build/stage6_voice_lab_round1.txt)
 # all failed on the same fact: the first 20 ms belonged to the KNOCK (a sine
 # carries the power) or to a click with no stone under it. So the crack now
 # comes first and the knock lands 8-12 ms behind it.
 "SPLIT2": """
  S._burst(t, { freq: 2600, q: 0.8, gain: 0.10, dur: 0.035, type:"highpass" });
  S._burst(t, { freq: 900, q: 1.2, gain: 0.06, dur: 0.06, type:"bandpass" });
  S._tone (t + 0.012, { freq: 120, to: 60, gain: 0.05, dur: 0.09, type:"sine" });""",
 "SNAP": """
  S._burst(t, { freq: 3000, q: 1.0, gain: 0.12, dur: 0.025, type:"bandpass" });
  S._burst(t + 0.008, { freq: 350, q: 0.7, gain: 0.08, dur: 0.09, type:"lowpass" });""",
 "SPALL": """
  S._burst(t, { freq: 2000, q: 0.8, gain: 0.09, dur: 0.030, type:"highpass" });
  S._burst(t + 0.015, { freq: 1500, q: 2.0, gain: 0.04, dur: 0.020, type:"bandpass" });
  S._burst(t + 0.030, { freq: 2300, q: 2.0, gain: 0.04, dur: 0.020, type:"bandpass" });
  S._tone (t + 0.010, { freq: 140, to: 70, gain: 0.045, dur: 0.08, type:"sine" });""",
}
# The ratchet: `clicks` are [offset, freq] pairs; the boom follows at `bt`.
CAST = {
 # ROUND 4. Rounds 1-3's three (the same shapes; runs/build/stage6_voice_lab_round3b.txt)
 # put the RATCHET 26-29 dB under the blow once the boom was level-matched --
 # on a phone, 2 dB over the bow's own release, so the cast read as a boom
 # alone. "A ratchet INTO a boom" is two sounds; the clicks are doubled (+6 dB)
 # and the rule now measures the ratchet by itself.
 "PAWL2": """
  const K = [[0,2300],[0.050,2300],[0.095,2350],[0.135,2400],[0.170,2450],[0.200,2500],[0.226,2550],[0.248,2600],[0.266,2650]];
  for (const [d, f] of K){
    S._burst(t + d, { freq: f, q: 3.0, gain: 0.12, dur: 0.012, type:"bandpass" });
    S._tone (t + d, { freq: f * 0.39, gain: 0.040, dur: 0.020, type:"triangle" });
  }
  S._tone (t + 0.28, { freq: 64, to: 30, gain: 0.22, dur: 0.34, type:"sine" });
  S._burst(t + 0.28, { freq: 180, q: 0.6, gain: 0.16, dur: 0.30, type:"lowpass" });""",
 "CRANK2": """
  for (let i = 0; i < 7; i++){
    const d = i * 0.035, f = 1800 + i * 130;
    S._burst(t + d, { freq: f, q: 3.0, gain: 0.11, dur: 0.012, type:"bandpass" });
    S._tone (t + d, { freq: f * 0.39, gain: 0.036, dur: 0.020, type:"triangle" });
  }
  S._burst(t + 0.26, { freq: 700, q: 1.0, gain: 0.05, dur: 0.06, type:"bandpass" });
  S._tone (t + 0.26, { freq: 58, to: 28, gain: 0.20, dur: 0.38, type:"sine" });
  S._burst(t + 0.26, { freq: 220, q: 0.6, gain: 0.12, dur: 0.28, type:"lowpass" });""",
 "WINDLASS2": """
  S._tone (t, { freq: 180, to: 260, gain: 0.040, dur: 0.25, type:"sawtooth" });
  for (let i = 0; i < 6; i++){
    const d = i * 0.045;
    S._burst(t + d, { freq: 1500, q: 3.0, gain: 0.12, dur: 0.014, type:"bandpass" });
  }
  S._tone (t + 0.28, { freq: 70, to: 32, gain: 0.22, dur: 0.30, type:"sine" });
  S._burst(t + 0.28, { freq: 200, q: 0.6, gain: 0.14, dur: 0.26, type:"lowpass" });""",
}
WHISTLE = {
 "SINE": """
  const D = Math.max(0.12, Math.min(0.9, p.dur || 0.42));
  S._tone(t, { freq: 1900, to: 720, gain: 0.035, dur: D, type:"sine" });""",
 "REED": """
  const D = Math.max(0.12, Math.min(0.9, p.dur || 0.42));
  S._tone(t, { freq: 1500, to: 560, gain: 0.030, dur: D, type:"triangle" });""",
 "AIR": """
  const D = Math.max(0.12, Math.min(0.58, p.dur || 0.42));
  S._sweep(t, { f0: 2600, f1: 900, q: 9, gain: 0.060, dur: D, atk: D * 0.3 });""",
}
BURST = {
 # ROUND 2. Round 1's three (SLAB, QUARRY, SHOT; runs/build/stage6_voice_lab_round2.txt)
 # were audible 300-375 ms -- shorter than the nova (750) and Ironbloom's blast
 # (585), for the rarest sound in the relic (about one shell in fifteen bursts).
 # Same three shapes, rung out: the tones ~1.6x, the noise to the buffer's
 # 0.58, the rattle spread over half a second.
 "SLAB2": """
  S._tone (t, { freq: 86, to: 30, gain: 0.22, dur: 1.00, type:"sine" });
  S._burst(t, { freq: 260, q: 0.7, gain: 0.22, dur: 0.58, type:"lowpass" });
  [[0.06,1400],[0.11,2200],[0.16,1700],[0.23,2600],[0.29,1500],[0.36,2000],[0.43,1800],[0.50,2400]].forEach(([d, f]) =>
    S._burst(t + d, { freq: f, q: 2.5, gain: 0.040, dur: 0.030, type:"bandpass" }));""",
 "QUARRY2": """
  S._tone (t, { freq: 70, to: 26, gain: 0.25, dur: 1.10, type:"sine" });
  S._burst(t, { freq: 200, q: 0.6, gain: 0.20, dur: 0.58, type:"lowpass" });
  S._burst(t, { freq: 900, q: 0.9, gain: 0.08, dur: 0.12, type:"bandpass" });
  for (let i = 0; i < 10; i++)
    S._burst(t + 0.05 + i * 0.047 + (i % 3) * 0.009, { freq: 2800, q: 0.8, gain: 0.030, dur: 0.020, type:"highpass" });""",
 "SHOT2": """
  S._tone (t, { freq: 100, to: 36, gain: 0.20, dur: 0.90, type:"sine" });
  S._burst(t, { freq: 500, q: 0.8, gain: 0.18, dur: 0.45, type:"bandpass" });
  [0.07, 0.14, 0.22, 0.31, 0.40, 0.48, 0.55].forEach((d, i) =>
    S._burst(t + d, { freq: 1800, q: 3.0, gain: 0.050 - i * 0.005, dur: 0.040, type:"bandpass" }));""",
}


def transpose(body: str, ratio: float, stretch: float) -> str:
    """The thud pitched down: every freq/to x ratio, every dur x stretch."""
    import re
    def fr(m):
        return f"{m.group(1)}: {round(float(m.group(2)) * ratio, 2):g}"
    def du(m):
        return f"dur: {round(float(m.group(1)) * stretch, 3):g}"
    out = re.sub(r"\b(freq|to): ([\d.]+)", fr, body)
    return re.sub(r"\bdur: ([\d.]+)", du, out)


def reverse_ratchet(cast_body: str) -> dict:
    """The ratchet reversed: the picked cast's clicks, last first, the gaps
    mirrored so it DECELERATES, pitched down a fifth, at 0.7, and no boom."""
    import re
    m = re.search(r"const K = (\[\[.*?\]\]);", cast_body)
    if m:
        K = json.loads(m.group(1))
    else:
        K = None
    return K


# ---------------------------------------------------------------- RENDER ---
RENDER_JS = r"""async ([evs, secs, seed, useBuild]) => {
  const sr = 48000, proto = Object.getPrototypeOf(AC.SFX);
  const oc = new OfflineAudioContext(1, Math.round(sr * secs), sr);
  let cursor = 0;
  const S = Object.create(proto);
  S.ok = true; S.on = true;
  S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
    const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
  S.bus = S.constructor.buildChain(oc, oc.destination);
  const n = Math.floor(sr * 0.6), nb = oc.createBuffer(1, n, sr), d = nb.getChannelData(0);
  let s = (seed || 0x9e3779b9) >>> 0;
  for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; d[i] = (s / 4294967296) * 2 - 1; }
  S.noise = nb;
  for (const e of evs){
    cursor = e.at;
    if (e.play) S.play(e.play[0], e.play[1] || {});
    else { const f = new Function("S", "t", "p", e.body); f(S, e.at, e.p || {}); }
  }
  const buf = await oc.startRendering(), x = buf.getChannelData(0);
  const u8 = new Uint8Array(x.buffer, x.byteOffset, x.byteLength);
  let str = ""; for (let i = 0; i < u8.length; i += 0x8000) str += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(str);
}"""

SEEDS = [0x9e3779b9, 0x1234567, 0xdeadbeef, 0x51f15eed]


def render(page, evs, secs=3.0, seed=SEEDS[0]):
    b64 = page.evaluate(RENDER_JS, [evs, secs, seed, False])
    return np.frombuffer(base64.b64decode(b64), dtype=np.float32).copy()


# --------------------------------------------------------------- MEASURE ---
def rms_track(x, win, hop):
    n = len(x); out = []; ts = []
    for i in range(0, n - win, hop):
        seg = x[i:i + win]; out.append(math.sqrt(float(np.mean(seg * seg)) + 1e-20)); ts.append((i + win / 2) / SR)
    return np.array(out), np.array(ts)


def db(v):
    return 20 * math.log10(max(v, 1e-12))


BANDS = [25 * 2 ** (k / 3) for k in range(31) if 25 * 2 ** (k / 3) <= 16000]


def measure(x):
    y = x[int(T0 * SR):]
    e5, t5 = rms_track(y, 240, 240)
    e50, t50 = rms_track(y, 2400, 240)
    if e5.max() < 1e-7:
        return {"silent": True}
    th = e5.max() * 0.02
    idx = np.where(e5 > th)[0]
    a0, a1 = t5[idx[0]] - 0.0025, t5[idx[-1]] + 0.0025
    top_i = int(np.argmax(e50))
    seg = y[max(0, int(a0 * SR)):int(a1 * SR) + 1]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n=1 << int(math.ceil(math.log2(max(len(seg), 4096)))))) ** 2
    f = np.fft.rfftfreq((len(spec) - 1) * 2, 1 / SR)
    cent = float((spec * f).sum() / spec.sum())
    low = float(spec[f < 150].sum() / spec.sum())
    s60 = y[max(0, int(a0 * SR)):max(0, int(a0 * SR)) + int(0.06 * SR)]
    sp60 = np.abs(np.fft.rfft(s60 * np.hanning(len(s60)), n=8192)) ** 2
    f60 = np.fft.rfftfreq(8192, 1 / SR)
    low60 = float(sp60[f60 < 150].sum() / max(sp60.sum(), 1e-20))
    # PHONE: the loudest 50 ms of what a phone speaker reproduces -- the voice
    # high-passed at 200 Hz. The deliverable is watched on phones, and a thud
    # that is all under 150 Hz is a thud nobody hears there.
    Y = np.fft.rfft(y); fy = np.fft.rfftfreq(len(y), 1 / SR); Y[fy < 200] = 0
    yp = np.fft.irfft(Y, n=len(y)); ep, _ = rms_track(yp, 2400, 240)
    phone = db(float(ep.max()))
    s20 = y[max(0, int(a0 * SR)):max(0, int(a0 * SR)) + int(0.02 * SR)]
    sp20 = np.abs(np.fft.rfft(s20 * np.hanning(len(s20)), n=8192)) ** 2
    hi20 = float(sp20[f60 > 1000].sum() / max(sp20.sum(), 1e-20))
    bands = []
    for c in BANDS:
        lo, hi = c / 2 ** (1 / 6), c * 2 ** (1 / 6)
        bands.append(math.sqrt(float(spec[(f >= lo) & (f < hi)].sum()) + 1e-20))
    # the ratchet: transients in the >1 kHz envelope in the first 300 ms
    hp = np.diff(y[:int(0.30 * SR) + 1])
    env, te = rms_track(hp, 48, 48)
    thr = env.max() * 0.25 if env.max() > 0 else 1
    clicks, last = 0, -1.0
    for i in range(1, len(env) - 1):
        if env[i] > thr and env[i] >= env[i - 1] and env[i] >= env[i + 1] and te[i] - last > 0.008:
            clicks += 1; last = te[i]
    # the glide: pitch in the first and last quarter of the audible span
    def peak_f(s):
        if len(s) < 512: return float("nan")
        sp = np.abs(np.fft.rfft(s * np.hanning(len(s)), n=1 << 16)); ff = np.fft.rfftfreq(1 << 16, 1 / SR)
        m = (ff > 200) & (ff < 6000); k = np.argmax(sp * m); return float(ff[k])
    q = (a1 - a0) / 4
    fa = peak_f(y[int(a0 * SR):int((a0 + q) * SR)]); fb = peak_f(y[int((a1 - q) * SR):int(a1 * SR)])
    glide = 12 * math.log2(fb / fa) if fa > 0 and fb > 0 else float("nan")
    return {"peak": float(np.abs(y).max()), "top": db(float(e50[top_i])), "topAt": float(t50[top_i] - a0),
            "aud": float(a1 - a0), "gone": float(a1), "cent": cent, "low": low, "low60": low60, "hi20": hi20, "phone": phone,
            "bands": bands, "clicks": clicks, "glide": glide, "pre": float(np.abs(x[:int(T0 * SR) - 10]).max())}


def reg(a, b):
    va, vb = np.array(a["bands"]), np.array(b["bands"])
    return float((va * vb).sum() / math.sqrt((va * va).sum() * (vb * vb).sum()))


def worst(page, body=None, play=None, p=None, dur=3.0):
    """Render on four noise draws; return the measurement of the LOUDEST
    (worst for a quiet voice) and of the median, and the first draw's PCM."""
    ms, pcm0 = [], None
    for sd in SEEDS:
        ev = {"at": T0}
        if play: ev["play"] = play
        else: ev["body"] = body; ev["p"] = p or {}
        x = render(page, [ev], dur, sd)
        if pcm0 is None: pcm0 = x
        ms.append(measure(x))
    if any(m.get("silent") for m in ms):
        raise SystemExit(f"SILENT render: {play or body[:60]}")
    if any(m["pre"] > 1e-6 for m in ms):
        raise SystemExit("something sounded before t = 1.0")
    loud = max(ms, key=lambda m: m["top"])
    return loud, ms, pcm0


def fmt(m, hit=None):
    s = (f"peak {m['peak']:.3f}  TOP {m['top']:6.1f} dB @ {m['topAt']*1000:4.0f} ms  aud {m['aud']*1000:4.0f} ms  "
         f"cent {m['cent']:6.0f} Hz  low {m['low']:.2f}  low60 {m['low60']:.2f}  hi20 {m['hi20']:.2f}  PHONE {m['phone']:6.1f}")
    if hit is not None:
        s += f"  vs HIT {m['top'] - hit['top']:+5.1f} dB"
    return s


def scale_gains(body: str, k: float) -> str:
    """Every `gain: X` x k, rounded to 4 significant figures -- rounded BEFORE
    the render that is measured, so what ships is bit-for-bit what was."""
    import re
    def g(mm):
        v = float(mm.group(1)) * k
        return f"gain: {float(f'{v:.4g}'):g}"
    return re.sub(r"\bgain: ([\d.]+)", g, body)


def level_match(page, body, target, p=None, passes=4):
    """Solve the body's gains so its TOP (worst of four noise draws) lands on
    `target` dB. The pick is then made on SHAPE (zenith_voice_lab's method).
    The compressor is in the chain, so this iterates rather than solving once."""
    b = body
    for _ in range(passes):
        m = worst(page, body=b, p=p)[0]
        err = target - m["top"]
        if abs(err) < 0.25:
            return b, m
        b = scale_gains(b, 10 ** (err / 20))
    return b, worst(page, body=b, p=p)[0]


def strip_bands(v):
    return {kk: vv for kk, vv in v.items() if kk != "bands"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--shipped", action="store_true")
    a = ap.parse_args()
    out = {}
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"CULVERIN'S VOICES -- {a.game} -- Chromium {ver} -- OfflineAudioContext 48 kHz, "
              f"event at t = 1.0, through Sfx.buildChain, xorshift noise, worst of {len(SEEDS)} draws\n")
        C = {}
        for name, play in [("hit@21.6", ["hit", {"dmg": 21.6}]), ("hit@13.5", ["hit", {"dmg": 13.5}]),
                           ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}]),
                           ("ironbloom blast", ["ult", {"w": "slagheart-blast"}]), ("nova", ["nova", {}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<16} {fmt(C[name])}")
        hit = C["hit@21.6"]
        H = hit["top"]
        out["controls"] = {k: strip_bands(v) for k, v in C.items()}
        print("\n  rune-crack is what Culverin's cast plays until stage 6 (an id with no arm, the shared fallback).")
        print("  EVERY CANDIDATE IS LEVEL-MATCHED to its voice's target before it is judged, so the pick is on SHAPE.")

        def run(label, cands, target, rule, why, ctrls, p=None):
            print(f"\n{label}   -- " + (f"level-matched to HIT {target - H:+.0f} dB" if target is not None
                                             else "NOT level-matched: the cast's own ratchet level x 0.7"))
            R, B = {}, {}
            for name, body in cands.items():
                if target is None:
                    b, m = body, worst(page, body=body, p=p)[0]
                else:
                    b, m = level_match(page, body, target, p)
                R[name], B[name] = m, b
                regs = "  ".join(f"REG {c} {reg(m, v):.2f}" for c, v in ctrls.items())
                print(f"  {name:<9} {fmt(m, hit)}  clicks {m['clicks']}  glide {m['glide']:+.1f} st\n            {regs}")
            ok = {k: m for k, m in R.items() if rule(k, m, B[k])}
            pick = why(ok) if ok else None
            print(f"  PICK  {pick if pick else 'NONE -- no candidate passes the rule'}")
            return R, B, pick

        def keep(key, R, B, pick):
            out[key] = {"pick": pick, "body": B.get(pick), "rows": {k: strip_bands(v) for k, v in R.items()}}

        # THE THUD, at HIT -12 dB: the heaviest basic-attack voice in the game
        # (the arrow's loose sits 31 dB under the blow) and still UNDER the
        # blow, because a shot leaving must read quieter than one landing (the
        # bow's own loose comment). Rule: audible 60-220 ms ("short"); LOW >= 0.6
        # ("deep"); REG <= 0.85 against the arrow's loose and against the blow
        # itself (a thud, not a second hit); PHONE >= the arrow's loose + 6 dB
        # (heard over the bow's release ON A PHONE, which reproduces little under
        # 200 Hz -- round 3's correction: rounds 1-2 picked on centroid alone and
        # took the least audible thud on the device the video is made for). Of
        # the passers, the lowest centroid ("a cannon at a distance").
        R, B, thud = run("THE THUD  (loose, spell:\"slug\")  -- \"a deep short thud on leaving (a cannon at a distance)\"",
                         THUD, H - 12,
                         lambda k, m, b: 0.06 <= m["aud"] <= 0.22 and m["low"] >= 0.6
                                      and reg(m, C["arrow loose"]) <= 0.85 and reg(m, hit) <= 0.85
                                      and m["phone"] >= C["arrow loose"]["phone"] + 6,
                         lambda ok: min(ok, key=lambda k: ok[k]["cent"]),
                         {"arrow loose": C["arrow loose"], "hit@21.6": hit})
        keep("thud", R, B, thud)
        # THE CRACK, at HIT -16 dB (about sixty a fight; the wall tick sits 22
        # under). Rule: audible <= 130 ms; HI20 >= 0.25 (it OPENS bright -- a
        # centroid over the whole voice is swamped by the knock); LOW >= 0.2
        # (stone, not a click: the wall tick's LOW is 0.00); REG <= 0.85 against
        # the wall tick. Of the passers, the highest HI20.
        R, B, crack = run("THE CRACK  (slug-land)  -- \"a stone crack on landing\"", CRACK, H - 16,
                          lambda k, m, b: m["aud"] <= 0.13 and m["hi20"] >= 0.25 and m["low"] >= 0.2
                                       and reg(m, C["wall"]) <= 0.85 and m["phone"] >= C["arrow loose"]["phone"],
                          lambda ok: max(ok, key=lambda k: ok[k]["hi20"]),
                          {"wall": C["wall"], "hit@21.6": hit})
        keep("crack", R, B, crack)
        # THE CAST, at HIT +0 dB (rune-crack's own level). Rule: audible
        # 0.35-0.70 s; >= 6 clicks in the first 300 ms (a ratchet, not a
        # strike); the TOP after 250 ms (the boom comes AFTER the ratchet);
        # LOW >= 0.35; REG <= 0.5 against rune-crack; PHONE within 6 dB of the
        # blow's (round 3: the cast ANNOUNCES the ultimate, and PAWL -- the most
        # clicks -- put its boom under what a phone reproduces, 11 dB under a
        # hit there); and the RATCHET BY ITSELF (the boom removed) within 12 dB
        # of the blow on a phone (round 4: "a ratchet into a boom" is two
        # sounds, and the level-matched boom had buried the first). Of the
        # passers, the MOST clicks -- the ratchet is what the voice is;
        # register breaks a tie.
        R, B, cast = run("THE CAST  (ult culverin)  -- \"a mechanical ratchet into a low boom, 0.4s\"", CAST, H,
                         lambda k, m, b: 0.35 <= m["aud"] <= 0.70 and m["clicks"] >= 6 and m["topAt"] >= 0.25
                                      and m["low"] >= 0.35 and reg(m, C["rune-crack"]) <= 0.5
                                      and m["phone"] >= hit["phone"] - 6
                                      and worst(page, body=ratchet_of(b))[0]["phone"] >= hit["phone"] - 12,
                         lambda ok: max(ok, key=lambda k: (ok[k]["clicks"], -reg(ok[k], C["rune-crack"]))),
                         {"rune-crack": C["rune-crack"], "hit@21.6": hit})
        keep("cast", R, B, cast)
        if not (thud and crack and cast):
            raise SystemExit("a voice has no pick -- the rule or the candidates are wrong; nothing to ship")
        # THE SHELL: "the thud pitched down" -- the PICKED thud a fifth or an
        # octave down, 1.25x as long, at HIT -8 dB (a bigger launch than a
        # slug's). Rule: REG <= 0.95 against the thud (heard as a different,
        # bigger event); PHONE at least the arrow's loose (every voice's floor --
        # round 3 first asked for "within 3 dB of the thud", which a voice
        # defined as PITCHED DOWN cannot keep). Of the passers, the one with
        # more LOW.
        tm = worst(page, body=out["thud"]["body"])[0]
        SH = {"FIFTH": transpose(out["thud"]["body"], 2 ** (-7 / 12), 1.25),
              "OCTAVE": transpose(out["thud"]["body"], 0.5, 1.25)}
        R, B, shell = run("THE SHELL  (ult culverin-shell)  -- \"the thud pitched down\"", SH, H - 8,
                          lambda k, m, b: reg(m, tm) <= 0.95 and m["phone"] >= C["arrow loose"]["phone"],
                          lambda ok: max(ok, key=lambda k: ok[k]["low"]),
                          {"the thud": tm})
        keep("shell", R, B, shell)
        # THE WHISTLE, over the flight a shell has left at its apex (~0.42 s),
        # at HIT -18 dB (over the fight, under the blow). Rule: it FALLS (GLIDE
        # <= -5 st); audible within 25% of its flight. Of the passers, the
        # largest fall.
        R, B, whistle = run("THE WHISTLE  (ult culverin-whistle, dur 0.42)  -- \"a whistle on the way down\"",
                            WHISTLE, H - 18,
                            lambda k, m, b: m["glide"] <= -5 and abs(m["aud"] - 0.42) <= 0.105
                                         and m["phone"] >= C["arrow loose"]["phone"],
                            lambda ok: min(ok, key=lambda k: ok[k]["glide"]),
                            {"hit@21.6": hit}, p={"dur": 0.42})
        keep("whistle", R, B, whistle)
        # THE BURST, at HIT +2 dB (the ultimate's punctuation: the nova sits at
        # +0.4, Ironbloom's blast at +5.9). Rule: audible 0.40-0.95 s; LOW60 >=
        # 0.5 (a bass hit); >= 4 clicks (the stone rattle); REG <= 0.90 against
        # Ironbloom's blast AND the nova (it must be neither). Of the passers,
        # the lowest of those two registers.
        R, B, burst = run("THE BURST  (ult culverin-burst)  -- \"a bass hit with a stone rattle\"", BURST, H + 2,
                          lambda k, m, b: 0.40 <= m["aud"] <= 0.95 and m["low60"] >= 0.5 and m["clicks"] >= 4
                                       and reg(m, C["ironbloom blast"]) <= 0.90 and reg(m, C["nova"]) <= 0.90
                                       and m["phone"] >= hit["phone"] - 6,
                          lambda ok: min(ok, key=lambda k: max(reg(ok[k], C["ironbloom blast"]), reg(ok[k], C["nova"]))),
                          {"ironbloom blast": C["ironbloom blast"], "nova": C["nova"], "hit@21.6": hit})
        keep("burst", R, B, burst)
        # THE CLOSE: "the ratchet reversed" -- the picked cast's own clicks run
        # backwards (so it DECELERATES), a fifth down, no boom; and the same with
        # a small release. NOT LEVEL-MATCHED: its clicks are the cast's own at
        # 0.7, because matching it to the WHOLE cast (whose level is the boom)
        # drove round 2's clicks ~20 dB over the cast's own ratchet. Rule: >= 5
        # clicks; audible 0.20-0.50 s; REG <= 0.95 against the cast; TOP at
        # least 1 dB under the cast's RATCHET (the boom removed). BACK over
        # RELEASE when both pass: the design says reversed, not
        # reversed-and-something.
        cm = worst(page, body=out["cast"]["body"])[0]
        rm = worst(page, body=ratchet_of(out["cast"]["body"]))[0]
        print(f"\n  the cast's RATCHET alone (its boom removed): {fmt(rm, hit)}")
        CL = close_bodies(out["cast"]["body"])
        R, B, close = run("THE CLOSE  (ult culverin-close)  -- \"the ratchet reversed\"", CL, None,
                          lambda k, m, b: m["clicks"] >= 5 and 0.20 <= m["aud"] <= 0.50 and reg(m, cm) <= 0.95
                                       and m["top"] <= rm["top"] - 1 and m["phone"] >= C["arrow loose"]["phone"],
                          lambda ok: "BACK" if "BACK" in ok else next(iter(ok)),
                          {"the cast": cm})
        keep("close", R, B, close)

        picks = {k: out[k]["body"] for k in ("thud", "crack", "cast", "shell", "whistle", "burst", "close")}
        if not all(picks.values()):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k, v in picks.items() if not v))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies, sample for sample:")
            bad = 0
            for key, play, pp in [("thud", ["loose", {"spell": "slug"}], None), ("crack", ["slug-land", {}], None),
                                  ("cast", ["ult", {"w": "culverin"}], None), ("shell", ["ult", {"w": "culverin-shell"}], None),
                                  ("whistle", ["ult", {"w": "culverin-whistle", "dur": 0.42}], {"dur": 0.42}),
                                  ("burst", ["ult", {"w": "culverin-burst"}], None), ("close", ["ult", {"w": "culverin-close"}], None)]:
                xs = render(page, [{"at": T0, "play": play}], 3.0)
                xc = render(page, [{"at": T0, "body": picks[key], "p": pp or {}}], 3.0)
                xc2 = render(page, [{"at": T0, "body": picks[key], "p": pp or {}}], 3.0)
                d = float(np.abs(xs - xc).max())
                # THE RENDERER'S OWN FLOOR. The same body in two fresh offline
                # contexts differs by up to ~6e-8 once a voice has more than a few
                # nodes (the graph's summation order), so "bit for bit" is not a
                # property this renderer has. The shipped arm must sit inside
                # that floor, and the floor itself under -120 dB.
                noise = float(np.abs(xc - xc2).max())
                ok = noise <= 1e-6 and d <= max(4 * noise, 1e-7)
                bad += not ok
                print(f"  {'ok  ' if ok else 'FAIL'}  {key:<8} max |shipped - picked| = {d:.3g}   "
                      f"the same body rendered twice: {noise:.3g}")
            if bad:
                raise SystemExit("the shipped arms are not the measured ones")
        assert not errors, errors
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


def ratchet_of(cast_body: str) -> str:
    """The cast with its boom removed: every line struck at the boom's own
    offset (the offset of the sine that falls), so the ratchet can be heard
    and measured by itself."""
    import re
    bt = re.search(r"S\._tone \(t \+ (0\.\d+), \{ freq: \d+, to:", cast_body).group(1)
    return "\n".join(l for l in cast_body.splitlines() if f"t + {bt}" not in l)


def close_bodies(cast_body: str) -> dict:
    """The ratchet reversed. Built from the picked cast's own click list, so it
    is that ratchet run backwards and not a new one."""
    import re
    K = reverse_ratchet(cast_body)
    if K is None:
        # CRANK / WINDLASS build their clicks in a loop: sample them the same way
        if "i * 0.035" in cast_body:
            K = [[i * 0.035, 1800 + i * 130] for i in range(7)]
        else:
            K = [[i * 0.045, 1500] for i in range(6)]
    end = K[-1][0]
    rev = [[round(end - d, 3), round(f * 2 ** (-7 / 12), 1)] for d, f in reversed(K)]
    ks = json.dumps(rev)
    # the click gains are the CAST's OWN (as level-matched) at 0.7
    gb = re.search(r"q: 3\.0, gain: ([\d.]+)", cast_body)
    gt = re.search(r"freq: f \* 0\.39, gain: ([\d.]+)", cast_body)
    g1 = float(f"{float(gb.group(1)) * 0.7:.4g}") if gb else 0.042
    g2 = float(f"{float(gt.group(1)) * 0.7:.4g}") if gt else 0.014
    back = f"""
  const K = {ks};
  for (const [d, f] of K){{
    S._burst(t + d, {{ freq: f, q: 3.0, gain: {g1:g}, dur: 0.012, type:"bandpass" }});
    S._tone (t + d, {{ freq: f * 0.39, gain: {g2:g}, dur: 0.020, type:"triangle" }});
  }}"""
    release = back + """
  S._tone (t + %s, { freq: 90, to: 60, gain: 0.05, dur: 0.15, type:"sine" });""" % round(end + 0.02, 3)
    return {"BACK": back, "RELEASE": release}


if __name__ == "__main__":
    sys.exit(main())
