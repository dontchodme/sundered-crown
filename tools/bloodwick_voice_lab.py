#!/usr/bin/env python
"""BLOODWICK'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v90.

    python bloodwick_voice_lab.py --game ../02-chain/sc-gyre-blade.html [--json out.json]
    python bloodwick_voice_lab.py --game ../02-chain/sc-bloodwick-fx.html --shipped

Design §6.2, every clause:
  cast    "a wet ignition -- a low whump into a candle-hiss, 0.35s."
  orbit   "nothing continuous (v75's rule: continuous voices are quiet or
          absent); a soft tick as each drop takes its slot."
  lunge   "one sharp wet crack (the release), then the spell's own hit voice
          per landing, pitched by count." The hit voice is the game's own; the
          crack is pitched by the count that lunged.
  close   "the hiss cut short."

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target
so the pick is on shape, the PHONE band (>200 Hz) as a floor, `--shipped`
checking the built arms against the picked bodies inside the renderer's own
floor. EVERY GAIN IS A LITERAL, so the level match can reach it (Crozier's
round 2, v95 build §6).

WHERE EACH ONE FIRES (bloodwick_build stage 6):
  cast   `ult {w:"bloodwick"}` -- fireUlt; Bloodwick fell through to the rune-crack
  slot   `ult {w:"bloodwick-slot"}` -- spawnShot, a globule taking its slot
  crack  `ult {w:"bloodwick-crack", n}` -- tickGyre, a lunge, n = how many lunged
  close  `ult {w:"bloodwick-close"}` -- tickGyre, the window running out by its
         clock, never a death
"""
from __future__ import annotations
import argparse, json, math, pathlib, re, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
from culverin_voice_lab import (render, measure, worst, level_match, reg, fmt, strip_bands, SEEDS, T0, SR,
                                rms_track, db)

HERE = pathlib.Path(__file__).parent

CAST = {
 # ROUND 2: round 1 (runs/build/stage6_voice_lab_round1.txt) ran every cast
 # 0.22-0.25 s against the design's 0.35; the hisses are longer, the whumps
 # unchanged.
 "WHUMP": """
  S._tone (t, { freq: 90, to: 50, gain: 0.10, dur: 0.14, type:"sine" });
  S._burst(t, { freq: 220, q: 0.7, gain: 0.06, dur: 0.10, type:"lowpass" });
  S._sweep(t + 0.05, { f0: 3000, f1: 6000, q: 0.8, gain: 0.03, dur: 0.42, atk: 0.08, type:"highpass" });""",
 "IGNITE": """
  S._burst(t, { freq: 600, q: 2.0, gain: 0.07, dur: 0.05, type:"bandpass" });
  S._tone (t, { freq: 130, to: 55, gain: 0.09, dur: 0.12, type:"triangle" });
  S._sweep(t + 0.04, { f0: 2500, f1: 5200, q: 0.9, gain: 0.03, dur: 0.42, atk: 0.07, type:"highpass" });""",
 "FLARE": """
  S._sweep(t, { f0: 180, f1: 90, q: 0.8, gain: 0.08, dur: 0.14, atk: 0.02, type:"lowpass" });
  S._tone (t, { freq: 110, to: 60, gain: 0.07, dur: 0.12, type:"sine" });
  S._sweep(t + 0.06, { f0: 3500, f1: 7000, q: 0.7, gain: 0.03, dur: 0.42, atk: 0.09, type:"highpass" });""",
}
SLOT = {
 "TICK": """
  S._burst(t, { freq: 2400, q: 4.0, gain: 0.03, dur: 0.015, type:"bandpass" });
  S._tone (t, { freq: 1400, gain: 0.01, dur: 0.03, type:"sine" });""",
 "DRIP": """
  S._tone (t, { freq: 1100, to: 1700, gain: 0.03, dur: 0.045, type:"sine" });""",
 "PLINK": """
  S._tone (t, { freq: 1760, gain: 0.025, dur: 0.05, type:"triangle" });""",
}
CRACK = {
 "CRACK": """
  const n = Math.max(1, Math.min(6, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 1800 * k, q: 1.5, gain: 0.08, dur: 0.04, type:"bandpass" });
  S._tone (t, { freq: 300 * k, to: 120, gain: 0.06, dur: 0.08, type:"sawtooth" });""",
 "SPLAT": """
  const n = Math.max(1, Math.min(6, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 900 * k, q: 1.0, gain: 0.08, dur: 0.06, type:"bandpass" });
  S._burst(t + 0.012, { freq: 2600 * k, q: 2.0, gain: 0.04, dur: 0.03, type:"bandpass" });
  S._tone (t, { freq: 200 * k, to: 90, gain: 0.05, dur: 0.08, type:"triangle" });""",
 "WHIP": """
  const n = Math.max(1, Math.min(6, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._sweep(t, { f0: 4000 * k, f1: 1200 * k, q: 1.2, gain: 0.07, dur: 0.07, atk: 0.005, type:"bandpass" });
  S._tone (t, { freq: 240 * k, to: 100, gain: 0.05, dur: 0.07, type:"sawtooth" });""",
}


def close_bodies(cast_body: str) -> dict:
    """THE HISS CUT SHORT: the picked cast's own hiss, alone, stopped early --
    its `_sweep` re-timed to start at once and end at 0.14 s (SHORT) or 0.20 s
    (SHORTER_CUT is the same hiss with a quicker attack)."""
    m = re.search(r"S\._sweep\(t \+ [\d.]+, \{ f0: ([\d.]+), f1: ([\d.]+), q: ([\d.]+), gain: ([\d.]+),", cast_body)
    f0, f1, q, g = m.groups()
    return {"SHORT": f'\n  S._sweep(t, {{ f0: {f0}, f1: {f1}, q: {q}, gain: {g}, dur: 0.14, atk: 0.03, type:"highpass" }});',
            "SHORT_SNAP": f'\n  S._sweep(t, {{ f0: {f0}, f1: {f1}, q: {q}, gain: {g}, dur: 0.20, atk: 0.01, type:"highpass" }});'}


def pitch(x):
    y = x[int(T0 * SR):int((T0 + 0.1) * SR)]
    sp = np.abs(np.fft.rfft(y * np.hanning(len(y)), n=1 << 16)); ff = np.fft.rfftfreq(1 << 16, 1 / SR)
    m = (ff > 200) & (ff < 8000)
    return float(ff[np.argmax(sp * m)])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--shipped", action="store_true")
    a = ap.parse_args()
    out = {}
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"BLOODWICK'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@7.8", ["hit", {"dmg": 7.75}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@7.8"]; H = hit["top"]; rel = C["arrow loose"]
        print("  (hit@7.8 is a globule landing: blade 7.75 x 1.0)")
        out["controls"] = {k: strip_bands(v) for k, v in C.items()}

        def run(label, cands, target, rule, why, ctrls, p=None, extra=None):
            print(f"\n{label}   -- " + (f"level-matched to HIT {target - H:+.0f} dB" if target is not None else "not level-matched"))
            R, B = {}, {}
            for name, body in cands.items():
                if target is None:
                    b, m = body, worst(page, body=body, p=p)[0]
                else:
                    b, m = level_match(page, body, target, p)
                e = extra(b, m) if extra else {}
                m.update(e)
                R[name], B[name] = m, b
                regs = "  ".join(f"REG {c} {reg(m, v):.2f}" for c, v in ctrls.items())
                ex = "  ".join(f"{k} {e[k]:.2f}" for k in e)
                print(f"  {name:<12} {fmt(m, hit)}  clicks {m['clicks']}\n               {regs}  {ex}")
            ok = {k: m for k, m in R.items() if rule(k, m, B[k])}
            pick = why(ok) if ok else None
            print(f"  PICK  {pick if pick else 'NONE -- no candidate passes the rule'}")
            return R, B, pick

        def keep(key, R, B, pick):
            out[key] = {"pick": pick, "body": B.get(pick), "rows": {k: strip_bands(v) for k, v in R.items()}}

        floor = rel["phone"]

        # THE CAST, at HIT -6. Rule: audible 0.25-0.50 s ("0.35s"); a low WHUMP
        # at its onset -- at least 20% of its first 60 ms under 150 Hz -- INTO a
        # hiss, which lifts its centroid over 800 Hz; REG <= 0.6 against the
        # rune-crack it replaces; PHONE within 12 dB of a hit (the whump alone
        # would vanish on a phone; the hiss is what carries). Of the passers,
        # the audible length nearest 0.35 s.
        R, B, cast = run("THE CAST  -- \"a wet ignition -- a low whump into a candle-hiss, 0.35s\"", CAST, H - 6,
                         lambda k, m, b: 0.25 <= m["aud"] <= 0.50 and m["low60"] >= 0.20 and m["cent"] >= 800
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: min(ok, key=lambda k: abs(ok[k]["aud"] - 0.35)),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)

        # THE SLOT, at HIT -22 ("a soft tick"; up to six a window). Rule:
        # audible <= 60 ms; PHONE at least the release's. Of the passers, the
        # shortest.
        R, B, slot = run("THE SLOT  -- \"a soft tick as each drop takes its slot\"", SLOT, H - 22,
                         lambda k, m, b: m["aud"] <= 0.06 and m["phone"] >= floor,
                         lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                         {"the release": rel})
        keep("slot", R, B, slot)

        # THE CRACK, at HIT -6 ("sharp"). Rule: audible <= 120 ms; PITCH at n=6
        # at least 3 semitones over n=1 (pitched by the count that lunged);
        # PHONE within 12 dB of a hit. Of the passers, the one least like the
        # hit voice that follows it on every landing.
        def rise(b, m):
            x1 = render(page, [{"at": T0, "body": b, "p": {"n": 1}}], 3.0)
            x6 = render(page, [{"at": T0, "body": b, "p": {"n": 6}}], 3.0)
            return {"rise": 12 * math.log2(pitch(x6) / pitch(x1))}
        R, B, crack = run("THE CRACK  -- \"one sharp wet crack (the release) ... pitched by count\"", CRACK, H - 6,
                          lambda k, m, b: m["aud"] <= 0.12 and m["rise"] >= 3 and m["phone"] >= hit["phone"] - 12,
                          lambda ok: min(ok, key=lambda k: reg(ok[k], hit)),
                          {"hit": hit}, p={"n": 1}, extra=rise)
        keep("crack", R, B, crack)

        # THE CLOSE: "the hiss cut short" -- the picked cast's own hiss, alone
        # and stopped early, at HIT -10. Rule: audible 0.06-0.20 s ("cut
        # short"); centroid over 2 kHz (it is the hiss); PHONE at least the
        # release's. Of the passers, the shortest.
        if out["cast"]["body"]:
            castm = worst(page, body=out["cast"]["body"])[0]
            R, B, close = run("THE CLOSE  -- \"the hiss cut short\"", close_bodies(out["cast"]["body"]), H - 10,
                              lambda k, m, b: 0.06 <= m["aud"] <= 0.20 and m["cent"] >= 2000 and m["phone"] >= floor,
                              lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                              {"the cast": castm})
            keep("close", R, B, close)
        keys = ("cast", "slot", "crack", "close")
        picks = {k: out[k]["body"] for k in keys if k in out}
        if not all(picks.values()) or len(picks) < len(keys):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in keys if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("cast", ["ult", {"w": "bloodwick"}], None), ("slot", ["ult", {"w": "bloodwick-slot"}], None),
                                  ("crack", ["ult", {"w": "bloodwick-crack", "n": 4}], {"n": 4}), ("close", ["ult", {"w": "bloodwick-close"}], None)]:
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
        pathlib.Path(a.json).write_bytes(json.dumps(out, indent=1).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
