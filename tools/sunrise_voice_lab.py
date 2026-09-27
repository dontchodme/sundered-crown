#!/usr/bin/env python
"""DAYBREAK'S VOICES, RENDERED AND SOLVED -- v99 §4.2's bounds, on the numbers.

    python sunrise_voice_lab.py --game ../02-chain/sc-sunrise.html [--solve]

Renders EXACTLY the text `sunrise_build.py` inserts (`voices_js`,
`tick_voice_js`, with its `VOICE` levels) through the shipped chain
(`Sfx.buildChain`) in an OfflineAudioContext, against a blow -- the `hit`
voice at Dawnbringer's own blade, 10.4 -- rendered the same way. Nothing here
is a second copy of a voice: the lab and the build cannot drift.

LEVEL is the loudest 50 ms RMS (5 ms hop) against the blow's, in dB -- the line's
measure (v97: "Loudest 50 ms: step 0 -16.8 dB"). The noise buffer is seeded, so
a render is repeatable; three seeds, and the median. AUDIBLE is first to last
5 ms RMS window above 2% of the voice's own loudest (v88's definition).

The design's bounds (§4.2): the arming -16 dB under a blow, re-struck every
0.25 s, and it STOPS on the break; the bell -4 dB, audible >= 400 ms, peak
within 15 ms; the shimmer -20 dB; the tick -10 dB; the sunset the shimmer's
top note held 0.4 s and released (~-34 dB 380 ms later).

`--solve` rescales each level to its target (three passes: the chain's
compressor is not linear near the top) and prints the VOICE dict to paste into
the builder. Without it, it measures what the builder holds.
"""
from __future__ import annotations
import argparse, json, math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import sunrise_build as SB

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-sunrise.html")
ap.add_argument("--solve", action="store_true")
ap.add_argument("--json", default=None)
a = ap.parse_args()

TARGET = {"hum": -16.0, "bell": -4.0, "up": -20.0, "tick": -10.0, "set": -18.0}

# A RENDER: a list of calls (time, fn, args) played into one offline context.
RENDER_JS = r"""async ([ultSrc, tickSrc, calls, secs, seed]) => {
  const OC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
  const S = Object.create(AC.SFX), sr = 44100;
  const off = new OC(1, Math.round(sr * secs), sr);
  let now = 1.0;
  const proxy = new Proxy(off, { get(o, k){
    if (k === 'currentTime') return now;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  S.ctx = proxy; S.ok = true; S.on = true;
  S.bus = AC.SFX.constructor.buildChain(off, off.destination);
  /* the noise, seeded: mulberry32 -- a render is repeatable */
  const real = Math.random;
  let s = seed >>> 0;
  Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  S.noise = S._noiseBuffer();
  Math.random = real;
  const ULT = new Function("t", "p", "w", "clamp", ultSrc + "}");
  const TICK = new Function("t", "p", "kind", "clamp", "if (false){}\n" + tickSrc + "}");
  const strikes = [];
  const oTone = S._tone;
  S._tone = function(t, o, d){ strikes.push([t, o.freq, o.gain]); return oTone.call(this, t, o, d); };
  for (const [at, fn, w, p] of calls){
    now = at;
    if (fn === "hit") AC.SFX.play.call(S, "hit", p || {});
    else if (fn === "ult") ULT.call(S, now, p || {}, w, clamp);
    else if (fn === "tick") TICK.call(S, now, p || {}, "sunrise-tick", clamp);
  }
  const buf = await off.startRendering();
  const d = buf.getChannelData(0);
  const W = Math.round(sr * 0.05), H = Math.round(sr * 0.005);
  let e50 = 0, e50at = 0;
  for (let i = 0; i + W <= d.length; i += H){
    let s2 = 0; for (let j = i; j < i + W; j++) s2 += d[j] * d[j];
    const r = Math.sqrt(s2 / W); if (r > e50){ e50 = r; e50at = i / sr; }
  }
  const W5 = Math.round(sr * 0.005), r5 = [];
  for (let i = 0; i + W5 <= d.length; i += W5){
    let s2 = 0; for (let j = i; j < i + W5; j++) s2 += d[j] * d[j];
    r5.push(Math.sqrt(s2 / W5));
  }
  const mx = Math.max.apply(null, r5);
  let first = -1, last = -1;
  r5.forEach((v, k) => { if (v > mx * 0.02){ if (first < 0) first = k; last = k; } });
  let peak = 0, peakAt = 0;
  for (let i = 0; i < d.length; i++){ const v = Math.abs(d[i]); if (v > peak){ peak = v; peakAt = i / sr; } }
  /* the level in 50 ms steps, for the shape of a train */
  const env = [];
  for (let i = 0; i + W <= d.length; i += W){
    let s2 = 0; for (let j = i; j < i + W; j++) s2 += d[j] * d[j];
    env.push(Math.sqrt(s2 / W));
  }
  return { e50, e50at, peak, peakAt, first: first * 0.005, last: (last + 1) * 0.005,
           env, strikes };
}"""


def db(x):
    return 20 * math.log10(max(x, 1e-9))


def ult_src(V):
    js = SB.voices_js(V)
    return js[: js.rindex('} else if (w === "widowmaker"){')] + "} else if (false){"


def tick_src(V):
    js = SB.tick_voice_js(V)
    return js[: js.rindex('else if (kind === "scour-tick"){')] + "else if (false){"


def hum_calls():
    """the cast at 1.0, a strike each quarter second of arming, the break at 5.0"""
    c = [(1.0, "ult", "dawnbringer", {})]
    for q in range(1, 16):                         # 0.25 .. 3.75 s of arming
        c.append((1.0 + 0.25 * q, "ult", "dawnbringer-arm", {"n": min(2, int(0.25 * q / 1.5))}))
    return c


SCENES = {
    "blow": ([(1.0, "hit", None, {"dmg": 10.4})], 2.0),
    "hum": (hum_calls(), 5.2),
    "bell": ([(1.0, "ult", "dawnbringer-break", {})], 3.0),
    "hum+break": (hum_calls() + [(5.0, "ult", "dawnbringer-break", {})], 7.0),
    "up": ([(1.0, "ult", "dawnbringer-break", {})]
           + [(1.0 + 0.5 * k, "ult", "dawnbringer-up", {}) for k in range(1, 9)], 6.0),
    "uponly": ([(1.0 + 0.5 * k, "ult", "dawnbringer-up", {}) for k in range(0, 8)], 6.0),
    "tick": ([(1.0, "tick", None, {})], 2.0),
    "set": ([(1.0, "ult", "dawnbringer-break", {}), (3.0, "ult", "dawnbringer-set", {})], 5.0),
}


def render(page, V, scene, seeds=(11, 23, 37)):
    calls, secs = SCENES[scene]
    out = [page.evaluate(RENDER_JS, [ult_src(V), tick_src(V), calls, secs, sd]) for sd in seeds]
    med = sorted(out, key=lambda r: r["e50"])[len(out) // 2]
    return med


def measure(page, V):
    R = {k: render(page, V, k) for k in SCENES}
    blow = R["blow"]["e50"]
    rel = {k: db(R[k]["e50"]) - db(blow) for k in R}
    return R, rel, blow


with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    V = dict(SB.VOICE)
    if a.solve:
        for p in range(4):
            R, rel, blow = measure(page, V)
            # the hum on its own train, the shimmer on the scene WITHOUT the bell
            got = {"hum": rel["hum"], "bell": rel["bell"], "up": rel["uponly"],
                   "tick": rel["tick"]}
            for k, key in (("hum", "hum"), ("bell", "bell"), ("up", "up")):
                V[key] *= 10 ** ((TARGET[k] - got[k]) / 20)
            fac = 10 ** ((TARGET["tick"] - got["tick"]) / 20)
            V["siz"] *= fac; V["chime"] *= fac
            V["mallet"] = V["bell"] / 3.0
            V["set"] = V["up"] * 1.25
            print(f"  pass {p + 1}: " + "  ".join(f"{k} {got[k]:+.2f}" for k in got))
        V = {k: float(f"{v:.4g}") for k, v in V.items()}
    R, rel, blow = measure(page, V)
    assert not errors, errors

print(f"\nDAYBREAK VOICES  {pathlib.Path(a.game).name}  Chromium {ver}   blow = hit at 10.4, "
      f"loudest 50 ms {db(blow):.1f} dBFS")
print(f"  VOICE = {json.dumps(V)}")
rows = [
    ("the arming (cast + 15 strikes, 3.75 s)", "hum", TARGET["hum"]),
    ("the bell, alone", "bell", TARGET["bell"]),
    ("the shimmer, 8 strikes, no bell", "uponly", TARGET["up"]),
    ("the tick", "tick", TARGET["tick"]),
]
for text, k, tgt in rows:
    r = R[k]
    print(f"  {text:<40} {rel[k]:+6.1f} dB  (target {tgt:+.0f})   peak at "
          f"{1000 * (r['peakAt'] - 1.0):6.1f} ms   audible {1000 * (r['last'] - r['first']):6.0f} ms")
hb = R["hum+break"]
after = [s for s in hb["strikes"] if s[0] > 5.0 + 1e-6 and s[1] in (220, 246.94, 261.63)]
bell = R["bell"]
print(f"  the hum after the break: {len(after)} strikes (it STOPS on the break)")
env = R["set"]["env"]
i0 = int(3.0 / 0.05)
seg = [db(v) for v in env[i0:i0 + 24]]
top = max(seg[:8]) if seg else -99
rel_ms = next((k * 50 for k, v in enumerate(seg) if k >= 8 and v < top - 34), None)
print(f"  the sunset: held {sum(1 for v in seg[:10] if v > top - 3) * 50} ms within 3 dB, "
      f"-34 dB at {rel_ms} ms after the set")
checks = [
    ("the arming at -16 +- 1.5 dB", abs(rel["hum"] - TARGET["hum"]) <= 1.5),
    ("the bell at -4 +- 1.5 dB, peak within 15 ms, audible >= 400 ms",
     abs(rel["bell"] - TARGET["bell"]) <= 1.5 and bell["peakAt"] - 1.0 <= 0.015
     and bell["last"] - bell["first"] >= 0.4),
    ("the shimmer at -20 +- 1.5 dB", abs(rel["uponly"] - TARGET["up"]) <= 1.5),
    ("the tick at -10 +- 1.5 dB", abs(rel["tick"] - TARGET["tick"]) <= 1.5),
    ("the hum stops on the break", len(after) == 0),
]
ok = sum(c for _, c in checks)
for t, c in checks:
    print(f"  {'PASS' if c else 'FAIL'}  {t}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(dict(V=V, rel=rel, chromium=ver), indent=1))
sys.exit(0 if ok == len(checks) else 1)
