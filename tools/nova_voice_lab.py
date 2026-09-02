"""THE NOVA'S VOICE, FITTED TO RICK'S REFERENCE BY MEASUREMENT.

    python nova_voice_lab.py --game ../02-chain/sc-crossweave.html

Rick supplied `Occultist Profane Boom Feels GOOD.wav` and named the two POPS in
it (2.2s and 3.9s), not the big hit at the end. This project has no sampler --
every voice is synthesised in WebAudio -- so a reference cannot be used, only
MEASURED and matched.

THE TARGET, from those two pops:

    peak position      40-190 ms after onset      (a swell, not a crack)
    decay to 10%       480-630 ms
    energy <120 Hz     56-64% over the whole pop
    energy <120 Hz     68-74% in the first 60 ms  (it OPENS low)
    centroid           520-710 Hz

THE LAST TWO ARE IN TENSION AND THAT IS THE WHOLE FITTING PROBLEM. A sound with
60% of its energy under 120 Hz has a centroid near 100 Hz unless something
quiet and bright sits on top of it -- so the fit needs a sub body carrying the
weight AND a thin high tail carrying the centroid, and getting one right while
ignoring the other is how a "matched" sound ends up nothing like the reference.

CANDIDATES ARE INJECTED, NOT BUILT. Nothing is written to any build; the winner
goes into `gloamwire_build.py` afterwards.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

# Rendered through `buildChain` -- the path that actually ships -- and
# scheduled at currentTime 1.0, both for `marrowdraw_relic_probe.SFX_JS`'s
# stated reasons: the chain's EQ and limiter move the profile, and an
# AudioParam anchored at t=0 behaves differently from one the game ever has.
RENDER_JS = r"""async ([body, secs]) => {
  const OC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
  if (!OC) return { skip: true };
  const S = AC.SFX, sr = 44100;
  const sv = { on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise };
  const off = new OC(1, Math.round(sr * secs), sr);
  S.ctx = off; S.ok = true; S.on = true;
  S.bus = S.constructor.buildChain(off, off.destination);
  S.noise = S._noiseBuffer();
  const proxy = new Proxy(off, { get(o, k){
    if (k === 'currentTime') return 1.0;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  S.ctx = proxy;
  let threw = null;
  try { (new Function('S', 't', body))(S, 1.0); }
  catch (e) { threw = String(e); }
  const buf = await off.startRendering();
  S.on = sv.on; S.ok = sv.ok; S.ctx = sv.ctx; S.bus = sv.bus; S.noise = sv.noise;
  const d = buf.getChannelData(0);
  const out = new Array(d.length);
  for (let i = 0; i < d.length; i++) out[i] = d[i];
  return { threw, sr, samples: out };
}"""

TARGET = dict(peak_ms=(40, 190), tail_ms=(480, 630), sub=(0.56, 0.64),
              sub60=(0.68, 0.74), centroid=(520, 710))


def measure(x, sr):
    x = np.asarray(x, dtype=np.float64)
    i0 = int(1.0 * sr)                      # scheduled at 1.0s
    x = x[i0:]
    if not len(x) or not np.abs(x).max():
        return None
    env = np.abs(x)
    k = max(1, int(0.004 * sr))
    env = np.convolve(env, np.ones(k) / k, mode="same")
    pk = env.max(); pi = int(env.argmax())
    idx = np.where(env > pk * 0.1)[0]
    tail = (idx[-1] - idx[0]) / sr if len(idx) else 0.0

    def bands(seg):
        if len(seg) < 64:
            return (0, 0, 0)
        w = seg * np.hanning(len(seg))
        S = np.abs(np.fft.rfft(w)) ** 2
        f = np.fft.rfftfreq(len(seg), 1 / sr)
        t = S.sum() or 1
        return ((f * S).sum() / t, S[f < 120].sum() / t, S[f >= 2000].sum() / t)
    end = min(len(x), int(1.2 * sr))
    cen, sub, hi = bands(x[:end])
    _, sub60, _ = bands(x[:int(0.06 * sr)])
    return dict(peak=float(pk), peak_ms=pi / sr * 1000, tail_ms=tail * 1000,
                centroid=cen, sub=sub, sub60=sub60, hi=hi)


def score(m):
    if not m:
        return 1e9
    s = 0.0
    for key, (lo, hi) in TARGET.items():
        v = m[key]
        if v < lo:  s += ((lo - v) / (hi - lo)) ** 2
        elif v > hi: s += ((v - hi) / (hi - lo)) ** 2
    return s


CANDS = {}
# AND THE LAST MISMATCH WAS THE TONES OUTLIVING THE NOISE. At burst `dur` 1.5
# the noise buffer runs dry at 0.6s while a 1.45s tone rings on, so the back
# half of the measured window is pure sub -- which is why the whole-clip figure
# read 88% below 120 Hz while the first 60 ms read 56%. The reference is the
# other way round: it OPENS sub-heavy (73%) and stays broadband (56% overall).
# So the body has to die with the noise rather than after it.
for _sub in (0.11, 0.15, 0.20):
    for _td in (0.95, 1.15):
        for _air in (0.22, 0.30):
            CANDS[f"sub{_sub:.2f} td{_td:.2f} air{_air:.2f}"] = f"""
              S._tone (t, {{ freq: 92, to: 30, gain: {_sub:.3f}, dur: {_td:.2f}, type:"sine" }});
              S._tone (t, {{ freq: 58, to: 24, gain: {_sub*0.75:.3f}, dur: {_td*1.1:.2f}, type:"sine" }});
              S._burst(t, {{ freq: 300, q: 0.7, gain: {_air:.3f}, dur: 1.50, type:"lowpass" }});
              S._burst(t, {{ freq: 1300, q: 0.7, gain: {_air*0.85:.3f}, dur: 1.30, type:"bandpass" }});
              S._burst(t, {{ freq: 3000, q: 0.8, gain: {_air*0.40:.3f}, dur: 0.75, type:"highpass" }});
            """


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
    ap.add_argument("--secs", type=float, default=2.6)
    a = ap.parse_args()
    gp = resolve_game(a.game)
    print("\n  TARGET, from the two pops Rick named\n")
    print(f"    {'peak at':>10}{'tail to10%':>12}{'<120Hz':>9}{'<120 @60ms':>12}"
          f"{'centroid':>10}")
    print(f"    {'40-190ms':>10}{'480-630ms':>12}{'56-64%':>9}{'68-74%':>12}"
          f"{'520-710':>10}\n")
    rows = []
    with game(game_path=gp) as (page, errors):
        for name, body in CANDS.items():
            r = page.evaluate(RENDER_JS, [body, a.secs])
            assert not errors, errors[:4]
            if r.get("skip"):
                raise SystemExit("no OfflineAudioContext in this runtime")
            if r.get("threw"):
                print(f"    {name:<18} THREW {r['threw']}")
                continue
            m = measure(r["samples"], r["sr"])
            rows.append((score(m), name, m))
            print(f"    {name:<18}{m['peak_ms']:>8.0f}ms{m['tail_ms']:>10.0f}ms"
                  f"{m['sub']:>9.1%}{m['sub60']:>12.1%}{m['centroid']:>10.0f}"
                  f"   peak {m['peak']:.3f}   fit {score(m):.2f}")
    rows.sort()
    print(f"\n  BEST FIT: {rows[0][1]}   (lower is closer; 0 is inside every band)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
