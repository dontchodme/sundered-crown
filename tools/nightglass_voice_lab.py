#!/usr/bin/env python
"""NIGHTGLASS'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v91.

    python nightglass_voice_lab.py --game ../02-chain/sc-backlash-blade.html [--json out.json]
    python nightglass_voice_lab.py --game ../02-chain/sc-nightglass-fx.html --shipped

Design §6.2, every clause:
  cast     "a reversed cymbal into a low glass tone, 0.4s."
  a blow   "the game's own hit voice, then 60ms later a dark echo of it (the
  taken    same voice, an octave down, filtered) -- the reflection IS the echo,
           and it is the only voice the mechanic needs."
  close    "the glass tone fading up and out."

The hit voice (`Sfx` kind "hit"): a bandpassed burst at 2600-1500w and a sine
falling from 190-90w to 46, w = clamp(dmg/45, 0.12, 1). The echo candidates are
that voice transposed an octave down and darkened, starting 60 ms late.

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target,
the PHONE band (>200 Hz) as a floor, `--shipped` checking the built arms inside
the renderer's own floor. Every gain is a literal the level match can reach.

WHERE EACH ONE FIRES (nightglass_build stage 6):
  cast   `ult {w:"nightglass"}` -- fireUlt; Nightglass fell through to the rune-crack
  echo   `ult {w:"nightglass-echo", dmg}` -- shroudBack, every blow thrown back,
         dmg = the blow thrown back (it rides 60 ms behind the hit voice)
  close  `ult {w:"nightglass-close"}` -- tickShroud, the window running out by
         its clock, never a death
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
 "REVCYM": """
  S._sweep(t, { f0: 5000, f1: 9000, q: 0.7, gain: 0.05, dur: 0.34, atk: 0.2, type:"highpass" });
  S._tone (t + 0.26, { freq: 220, gain: 0.06, dur: 0.42, type:"sine" });
  S._tone (t + 0.26, { freq: 663, gain: 0.018, dur: 0.28, type:"sine" });""",
 "SUCK": """
  S._sweep(t, { f0: 4000, f1: 8000, q: 0.7, gain: 0.02, dur: 0.30, atk: 0.18, type:"highpass" });
  S._sweep(t + 0.08, { f0: 5000, f1: 9500, q: 0.7, gain: 0.05, dur: 0.30, atk: 0.18, type:"highpass" });
  S._tone (t + 0.30, { freq: 165, gain: 0.07, dur: 0.44, type:"sine" });
  S._tone (t + 0.30, { freq: 498, gain: 0.02, dur: 0.30, type:"sine" });""",
 "GLASSRISE": """
  S._sweep(t, { f0: 1500, f1: 6000, q: 1.2, gain: 0.05, dur: 0.34, atk: 0.2, type:"bandpass" });
  S._tone (t + 0.27, { freq: 196, gain: 0.06, dur: 0.44, type:"sine" });
  S._tone (t + 0.27, { freq: 541, gain: 0.02, dur: 0.30, type:"sine" });""",
}
ECHO = {
 "ECHO": """
  const w = Math.max(0.12, Math.min(1, (p.dmg || 10) / 45)), e = t + 0.06;
  S._burst(e, { freq: (2600 - 1500 * w) / 2, q: 1.1, gain: 0.10, dur: 0.07 + 0.06 * w, type:"lowpass" });
  S._tone (e, { freq: (190 - 90 * w) / 2, to: 30, gain: 0.12, dur: 0.12 + 0.13 * w, type:"sine" });""",
 "DARK": """
  const w = Math.max(0.12, Math.min(1, (p.dmg || 10) / 45)), e = t + 0.06;
  S._burst(e, { freq: (2600 - 1500 * w) / 2, q: 1.1, gain: 0.10, dur: 0.07 + 0.06 * w, type:"bandpass" });
  S._tone (e, { freq: 190 - 90 * w, to: 60, gain: 0.08, dur: 0.12 + 0.13 * w, type:"triangle" });""",
 "HOLLOW": """
  const w = Math.max(0.12, Math.min(1, (p.dmg || 10) / 45)), e = t + 0.06;
  S._burst(e, { freq: (2600 - 1500 * w) / 2, q: 2.2, gain: 0.10, dur: 0.09 + 0.06 * w, type:"bandpass" });
  S._burst(e + 0.02, { freq: (2600 - 1500 * w) / 4, q: 1.4, gain: 0.06, dur: 0.08, type:"bandpass" });""",
}


def glass_tones(cast_body: str):
    """The picked cast's glass tone: its delayed `_tone`s, (freq, gain)."""
    return [(float(m.group(2)), float(m.group(3))) for m in
            re.finditer(r"S\._tone \(t \+ ([\d.]+), \{ freq: ([\d.]+), gain: ([\d.]+)", cast_body)]


def close_bodies(cast_body: str) -> dict:
    """THE GLASS TONE FADING UP AND OUT: its partials as narrow bands of noise
    that swell and cut off (Cipher's reversed chime, v94 build §6), one swell
    (SWELL) or two staggered (STAGGER: a single swell from -80 dB is heard for
    only its last fifth of a second)."""
    P = glass_tones(cast_body)
    def one(fr, g, t0, dur):
        return f'S._sweep(t + {t0:g}, {{ f0: {fr:g}, f1: {fr:g}, q: 40, gain: {g:g}, dur: {dur}, atk: {round(dur * 0.6, 3)}, type:"bandpass" }});'
    swell = "\n  " + "\n  ".join(one(fr, g, 0, 0.45) for fr, g in P)
    stag = "\n  " + "\n  ".join(one(fr, round(g * k, 5), round(i * 0.12, 3), 0.45) for i, k in enumerate((0.4, 1.0)) for fr, g in P)
    return {"SWELL": swell, "STAGGER": stag}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--shipped", action="store_true")
    a = ap.parse_args()
    out = {}
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"NIGHTGLASS'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@10", ["hit", {"dmg": 10}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@10"]; H = hit["top"]; rel = C["arrow loose"]
        print("  (hit@10 is a typical blow thrown back: half of a foe's ~20)")
        out["controls"] = {k: strip_bands(v) for k, v in C.items()}

        def run(label, cands, target, rule, why, ctrls, p=None):
            print(f"\n{label}   -- " + (f"level-matched to HIT {target - H:+.0f} dB" if target is not None else "not level-matched"))
            R, B = {}, {}
            for name, body in cands.items():
                b, m = level_match(page, body, target, p)
                R[name], B[name] = m, b
                regs = "  ".join(f"REG {c} {reg(m, v):.2f}" for c, v in ctrls.items())
                print(f"  {name:<12} {fmt(m, hit)}  clicks {m['clicks']}\n               {regs}")
            ok = {k: m for k, m in R.items() if rule(k, m, B[k])}
            pick = why(ok) if ok else None
            print(f"  PICK  {pick if pick else 'NONE -- no candidate passes the rule'}")
            return R, B, pick

        def keep(key, R, B, pick):
            out[key] = {"pick": pick, "body": B.get(pick), "rows": {k: strip_bands(v) for k, v in R.items()}}

        floor = rel["phone"]

        # THE CAST, at HIT -6. Rule: audible 0.35-0.45 s ("0.4s"); it SWELLS
        # rather than strikes -- its top at least 0.15 s in (round 1 asked the
        # back half, and a cymbal INTO a tone peaks where they meet, ~45% in,
        # with the tone ringing on after); REG <= 0.6 against the rune-crack it
        # replaces; PHONE within 12 dB of a hit. Of the passers, the loudest on
        # a phone.
        R, B, cast = run("THE CAST  -- \"a reversed cymbal into a low glass tone, 0.4s\"", CAST, H - 6,
                         lambda k, m, b: 0.35 <= m["aud"] <= 0.45 and m["topAt"] >= 0.15
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: max(ok, key=lambda k: ok[k]["phone"]),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)

        # THE ECHO, at HIT -6 (dmg 10; it rides behind the hit). Rule: DARKER --
        # its centroid at most 0.7x the hit's ("an octave down, filtered");
        # still THE SAME VOICE -- REG against the hit >= 0.4; HEARD ON A PHONE --
        # PHONE at least the release's (an octave down puts the hit's sine at
        # 23-50 Hz, where nobody hears it; the burst is what carries). Of the
        # passers, the one most like the hit.
        R, B, echo = run("THE ECHO  -- \"a dark echo of it (the same voice, an octave down, filtered)\"", ECHO, H - 6,
                         lambda k, m, b: m["cent"] <= 0.7 * max(hit["cent"], 400) and reg(m, hit) >= 0.4 and m["phone"] >= floor,
                         lambda ok: max(ok, key=lambda k: reg(ok[k], hit)),
                         {"hit": hit}, p={"dmg": 10})
        keep("echo", R, B, echo)

        # THE CLOSE: "the glass tone fading up and out", at HIT -10. Rule:
        # audible 0.25-0.60 s; its top in the back half (it fades UP); PHONE
        # within 6 dB of the release. Of the passers, the shorter.
        if out["cast"]["body"]:
            castm = worst(page, body=out["cast"]["body"])[0]
            R, B, close = run("THE CLOSE  -- \"the glass tone fading up and out\"", close_bodies(out["cast"]["body"]), H - 10,
                              lambda k, m, b: 0.25 <= m["aud"] <= 0.60 and m["topAt"] >= 0.5 * m["aud"] and m["phone"] >= floor - 6,
                              lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                              {"the cast": castm})
            keep("close", R, B, close)
        keys = ("cast", "echo", "close")
        picks = {k: out[k]["body"] for k in keys if k in out}
        if not all(picks.values()) or len(picks) < len(keys):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in keys if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("cast", ["ult", {"w": "nightglass"}], None), ("echo", ["ult", {"w": "nightglass-echo", "dmg": 14}], {"dmg": 14}),
                                  ("close", ["ult", {"w": "nightglass-close"}], None)]:
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
