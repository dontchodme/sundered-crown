#!/usr/bin/env python
"""BRIARWAND'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v93.

    python briarwand_voice_lab.py --game ../02-chain/sc-bloom-blade.html [--json out.json]
    python briarwand_voice_lab.py --game ../02-chain/sc-bloom-fx.html --shipped

Design §6.2, every clause:
  cast      "a soft exhale into a rustle, 0.4s (the bud opening)."
  the cloud "a very quiet sustained rustle while the foe is inside it (peak
            <= 0.12) -- like v75's sigil, the one continuous voice, quiet on
            purpose."
  a bite    "a short vegetable snap, pitched by entangle count."
  close     "the rustle fading."
The thorns' release is the bow's own (the design names no voice for it), one a
fan (the side thorns are quiet since stage 2).

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target
so the pick is on shape, the PHONE band (>200 Hz) as a floor -- every voice at
least as audible there as the bow's release -- and `--shipped` checking the
built arms against the picked bodies inside the renderer's own floor.

WHERE EACH ONE FIRES (briarwand_build stage 6):
  cast     `ult {w:"briarwand"}` -- fireUlt, for every relic; Briarwand fell
           through to the shared rune-crack until now
  rustle   `ult {w:"briarwand-rustle"}` -- tickPollen, re-struck every 0.25s of
           the window while the foe is inside the cloud (a held sound does not
           exist in this toolkit: CLAUDE.md 4.5)
  bite     `ult {w:"briarwand-bite", n}` -- tickPollen, every bite, n = the
           foe's entangle stacks after it
  close    `ult {w:"briarwand-close"}` -- tickPollen, the window running out by
           its clock, never a death
"""
from __future__ import annotations
import argparse, json, math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
from culverin_voice_lab import (render, measure, worst, level_match, reg, fmt, strip_bands, SEEDS, T0, SR,
                                rms_track, db)

HERE = pathlib.Path(__file__).parent

CAST = {
 "EXHALE": """
  S._sweep(t, { f0: 350, f1: 1400, q: 0.6, gain: 0.10, dur: 0.30, atk: 0.14, type:"bandpass" });
  [0.22, 0.27, 0.31, 0.36, 0.40].forEach((d, i) =>
    S._burst(t + d, { freq: 3200 + i * 300, q: 1.5, gain: 0.030, dur: 0.05, type:"bandpass" }));""",
 "BUDSIGH": """
  S._sweep(t, { f0: 600, f1: 2200, q: 0.8, gain: 0.09, dur: 0.38, atk: 0.20 });
  S._sweep(t + 0.18, { f0: 2600, f1: 5200, q: 1.2, gain: 0.05, dur: 0.26, atk: 0.08 });""",
 "PETAL": """
  S._sweep(t, { f0: 300, f1: 900, q: 0.5, gain: 0.11, dur: 0.24, atk: 0.12, type:"lowpass" });
  S._tone (t + 0.02, { freq: 520, to: 780, gain: 0.030, dur: 0.30, type:"sine" });
  [0.20, 0.25, 0.30, 0.35].forEach((d, i) =>
    S._burst(t + d, { freq: 2800 + i * 400, q: 1.8, gain: 0.028, dur: 0.05, type:"bandpass" }));""",
}
RUSTLE = {
 # ROUND 2. Round 1 (runs/build/stage6_voice_lab_round1.txt) struck three shapes
 # every 0.25 s and every one of them PULSED: 33-143 dB between the top and the
 # bottom of the 25 ms envelope, because every primitive in this toolkit decays
 # on an exponential ramp to -80 dB over its own length, so a strike has all
 # but gone by the next one. A sustained voice here is OVERLAPPING strikes:
 # each candidate names its own re-strike gap, and tickPollen strikes the
 # picked one at that gap.
 "LEAVES2": ("""
  S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.030, dur: 0.40, atk: 0.20 });""", 0.10),
 "HISS2": ("""
  S._burst(t, { freq: 4800, q: 0.7, gain: 0.020, dur: 0.50, type:"highpass" });""", 0.08),
 "AIRY": ("""
  S._sweep(t, { f0: 1800, f1: 2800, q: 0.7, gain: 0.030, dur: 0.50, atk: 0.25 });""", 0.12),
}
BITE = {
 "SNAP": """
  const n = Math.max(1, Math.min(4, p.n | 0));
  S._burst(t, { freq: 1700 + n * 220, q: 2.5, gain: 0.06, dur: 0.03, type:"bandpass" });
  S._tone (t, { freq: 620 + n * 90, to: 380 + n * 50, gain: 0.04, dur: 0.05, type:"triangle" });""",
 "STALK": """
  const n = Math.max(1, Math.min(4, p.n | 0));
  S._burst(t, { freq: 2600, q: 0.8, gain: 0.05, dur: 0.02, type:"highpass" });
  S._tone (t, { freq: 880 * Math.pow(2, (n - 1) * 2 / 12), to: 500, gain: 0.05, dur: 0.06, type:"sine" });""",
 "CELERY": """
  const n = Math.max(1, Math.min(4, p.n | 0)), k = Math.pow(2, (n - 1) * 2 / 12);
  S._burst(t, { freq: 1400 * k, q: 3.0, gain: 0.05, dur: 0.025, type:"bandpass" });
  S._burst(t + 0.012, { freq: 2600 * k, q: 3.0, gain: 0.04, dur: 0.025, type:"bandpass" });
  S._tone (t, { freq: 210, to: 140, gain: 0.03, dur: 0.05, type:"sine" });""",
}


def train(body: str, gap: float, secs=2.0) -> str:
    """The rustle as the cloud strikes it: re-struck every `gap` s for `secs`."""
    n = int(round(secs / gap))
    return f"for (let __i = 0; __i < {n}; __i++){{ (function(t){{ {body} }})(t + __i * {gap}); }}"


def fade_bodies(strike: str, gap: float) -> dict:
    """The close: the picked rustle's own strike at its own gap, falling
    linearly in dB to -24 over 0.8 s (FADE) or 1.2 s (FADE_LONG)."""
    def f(secs):
        n = int(round(secs / gap)); parts = []
        for i in range(n):
            k = round(10 ** (-24 * (i / max(1, n - 1)) / 20), 4)
            b = strike.replace("gain: ", f"gain: {k} * ")
            parts.append(f"(function(t){{ {b} }})(t + {round(i * gap, 3)});")
        return "\n  " + "\n  ".join(parts)
    return {"FADE": f(0.8), "FADE_LONG": f(1.2)}


def pitch(x):
    y = x[int(T0 * SR):int((T0 + 0.1) * SR)]
    sp = np.abs(np.fft.rfft(y * np.hanning(len(y)), n=1 << 16)); ff = np.fft.rfftfreq(1 << 16, 1 / SR)
    m = (ff > 200) & (ff < 6000)
    return float(ff[np.argmax(sp * m)])


def sustain(x, a=0.15, b=1.85):
    """p95 - p5 of the 25 ms RMS (dB) through a train: a sustained voice is flat."""
    y = x[int((T0 + a) * SR):int((T0 + b) * SR)]
    e, _ = rms_track(y, 1200, 240)
    d = 20 * np.log10(np.maximum(e, 1e-9))
    return float(np.percentile(d, 95) - np.percentile(d, 5))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--shipped", action="store_true")
    a = ap.parse_args()
    out = {}
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"BRIARWAND'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@9.2", ["hit", {"dmg": 9.15}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@9.2"]; H = hit["top"]
        print("  (hit@9.2 is a thorn landing: blade 15.25 x 0.6 -- the blow this relic lands most)")
        out["controls"] = {k: strip_bands(v) for k, v in C.items()}

        def run(label, cands, target, rule, why, ctrls, p=None, wrap=None, extra=None):
            print(f"\n{label}   -- " + (f"level-matched to HIT {target - H:+.0f} dB" if target is not None else "not level-matched"))
            R, B = {}, {}
            for name, body in cands.items():
                bb = wrap(body) if wrap else body
                if target is None:
                    b, m = bb, worst(page, body=bb, p=p)[0]
                else:
                    b, m = level_match(page, bb, target, p)
                e = extra(b, m) if extra else {}
                m.update(e)
                R[name], B[name] = m, b
                regs = "  ".join(f"REG {c} {reg(m, v):.2f}" for c, v in ctrls.items())
                ex = "  ".join(f"{k} {e[k]:.2f}" for k in e)
                print(f"  {name:<9} {fmt(m, hit)}  clicks {m['clicks']}\n            {regs}  {ex}")
            ok = {k: m for k, m in R.items() if rule(k, m, B[k])}
            pick = why(ok) if ok else None
            print(f"  PICK  {pick if pick else 'NONE -- no candidate passes the rule'}")
            return R, B, pick

        def keep(key, R, B, pick, body=None):
            out[key] = {"pick": pick, "body": body if body is not None else B.get(pick),
                        "rows": {k: strip_bands(v) for k, v in R.items()}}

        floor = C["arrow loose"]["phone"]
        # THE CAST, at HIT -6: "soft". Rule: audible 0.30-0.60 s ("0.4s"); the
        # TOP after 60 ms (an exhale swells, it does not strike); REG <= 0.6
        # against rune-crack; PHONE within 12 dB of a thorn's hit. Of the
        # passers, the latest TOP -- the softest onset.
        R, B, cast = run("THE CAST  -- \"a soft exhale into a rustle, 0.4s\"", CAST, H - 6,
                         lambda k, m, b: 0.30 <= m["aud"] <= 0.60 and m["topAt"] >= 0.06
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: max(ok, key=lambda k: ok[k]["topAt"]),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)
        # THE RUSTLE, judged as the cloud strikes it: eight strikes 0.25 s
        # apart, the train level-matched to HIT -20. Rule: the train's sample
        # PEAK <= 0.12 (the design's own number); SUSTAIN <= 10 dB (it does not
        # stutter); PHONE at least the bow's release. Of the passers, the
        # flattest (the lowest SUSTAIN).
        RB = {k: v[0] for k, v in RUSTLE.items()}
        GAP = {k: v[1] for k, v in RUSTLE.items()}
        trains = {k: train(RB[k], GAP[k]) for k in RB}
        R, B, rus = run("THE RUSTLE  -- \"a very quiet sustained rustle ... (peak <= 0.12)\"", trains, H - 20,
                        lambda k, m, b: m["peak"] <= 0.12 and m["sustain"] <= 10 and m["phone"] >= floor,
                        lambda ok: min(ok, key=lambda k: ok[k]["sustain"]),
                        {"wall": C["wall"]},
                        extra=lambda b, m: {"sustain": sustain(render(page, [{"at": T0, "body": b}], 3.0))})
        # the shipped rustle is ONE strike, re-struck at its gap by tickPollen:
        # un-wrap the level-matched train
        if rus:
            tb = B[rus]; strike = tb[tb.index("{ ", tb.index("function(t)")) + 2: tb.rindex(" })(t + __i")]
            keep("rustle", R, B, rus, body="\n" + strike)
            out["rustle"]["gap"] = GAP[rus]
            train_top = R[rus]["top"]
        else:
            keep("rustle", R, B, None)
        # THE BITE, at HIT -14 (about twelve a cast). Rule: audible <= 100 ms;
        # PITCH at n=4 at least 3 semitones over n=1 ("pitched by entangle
        # count"); PHONE at least the bow's release. Of the passers, the largest
        # rise -- the count is what the pitch is for.
        def bite_extra(b, m):
            x1 = render(page, [{"at": T0, "body": b, "p": {"n": 1}}], 3.0)
            x4 = render(page, [{"at": T0, "body": b, "p": {"n": 4}}], 3.0)
            return {"rise": 12 * math.log2(pitch(x4) / pitch(x1))}
        R, B, bite = run("THE BITE  -- \"a short vegetable snap, pitched by entangle count\"", BITE, H - 14,
                         lambda k, m, b: m["aud"] <= 0.10 and m["rise"] >= 3 and m["phone"] >= floor,
                         lambda ok: max(ok, key=lambda k: ok[k]["rise"]),
                         {"wall": C["wall"]}, p={"n": 1}, extra=bite_extra)
        keep("bite", R, B, bite)
        # THE CLOSE: "the rustle fading" -- the picked rustle's own strike at
        # its own gap, falling to -24 dB. Not level-matched (its level IS the
        # rustle's). Rule: audible 0.6-1.5 s; its TOP no louder than the
        # sustained rustle's (+0.5 dB). FADE over FADE_LONG when both pass.
        if out["rustle"]["body"]:
            rm = worst(page, body=out["rustle"]["body"])[0]
            CL = fade_bodies(out["rustle"]["body"].strip(), out["rustle"]["gap"])
            R, B, close = run("THE CLOSE  -- \"the rustle fading\"", CL, None,
                              lambda k, m, b: 0.6 <= m["aud"] <= 1.5 and m["top"] <= train_top + 0.5 and m["phone"] >= floor - 6,
                              lambda ok: "FADE" if "FADE" in ok else next(iter(ok)),
                              {"the rustle": rm})
            keep("close", R, B, close)
        picks = {k: out[k]["body"] for k in ("cast", "rustle", "bite", "close") if k in out}
        if not all(picks.values()) or len(picks) < 4:
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in ("cast", "rustle", "bite", "close") if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("cast", ["ult", {"w": "briarwand"}], None), ("rustle", ["ult", {"w": "briarwand-rustle"}], None),
                                  ("bite", ["ult", {"w": "briarwand-bite", "n": 3}], {"n": 3}), ("close", ["ult", {"w": "briarwand-close"}], None)]:
                xs = render(page, [{"at": T0, "play": play}], 3.0)
                xc = render(page, [{"at": T0, "body": picks[key], "p": pp or {}}], 3.0)
                xc2 = render(page, [{"at": T0, "body": picks[key], "p": pp or {}}], 3.0)
                d = float(np.abs(xs - xc).max()); noise = float(np.abs(xc - xc2).max())
                ok = noise <= 1e-6 and d <= max(4 * noise, 1e-7)
                bad += not ok
                print(f"  {'ok  ' if ok else 'FAIL'}  {key:<7} max |shipped - picked| = {d:.3g}   the same body twice: {noise:.3g}")
            if bad:
                raise SystemExit("the shipped arms are not the measured ones")
        assert not errors, errors
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
