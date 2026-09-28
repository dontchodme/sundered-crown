#!/usr/bin/env python
"""WATCHLIGHT'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v92.

    python watchlight_voice_lab.py --game ../02-chain/sc-beacon.html [--json out.json]
    python watchlight_voice_lab.py --game ../02-chain/sc-watchlight-fx.html --shipped

Design §6.2, every clause:
  cast          "a lamp being set down -- a wooden knock into a glass chime, 0.35s."
  a lantern     "the staff's own shot voice, filtered brighter and quieter (it
  shot         is the smaller bolt), pitched by the lantern's count."
  a shove       "the game's hit voice with a low thump under it when knock >= 400
                (one flag on the play)."
  close         "the chime reversed, short."
The wardbolt's release is the staff's own -- the bow's release, the 380 Hz
burst every staff shot without a voice of its own plays.

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target
so the pick is on shape, the PHONE band (>200 Hz) as a floor, and `--shipped`
checking the built arms against the picked bodies inside the renderer's own
floor.

WHERE EACH ONE FIRES (watchlight_build stage 6):
  cast   `ult {w:"watchlight"}` -- fireUlt, for every relic; Watchlight fell
         through to the shared rune-crack until now
  lamp   `ult {w:"watchlight-lamp", n}` -- tickBeacon, every lantern shot,
         n = its count in this window (1-7)
  thump  `ult {w:"watchlight-thump"}` -- the hit branch of tickShots, after
         the hit voice, on a WARDBOLT's landing (knock 420 >= 400). Its own
         arm rather than a flag on the shared hit voice, so no other relic's
         hit can change -- the same sound, one line further from everyone else.
  close  `ult {w:"watchlight-close"}` -- tickBeacon, the window running out by
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
 # ROUND 2. Round 1 (runs/build/stage6_voice_lab_round1.txt) ran every chime
 # 0.24-0.25 s against the design's 0.35 and each missed one rule narrowly;
 # the chimes are longer here, the knocks unchanged.
 "KNOCKCHIME": """
  S._burst(t, { freq: 520, q: 1.5, gain: 0.10, dur: 0.05, type:"bandpass" });
  S._tone (t, { freq: 240, to: 170, gain: 0.07, dur: 0.06, type:"triangle" });
  S._tone (t + 0.07, { freq: 1568, gain: 0.05, dur: 0.46, type:"sine" });
  S._tone (t + 0.07, { freq: 2349, gain: 0.025, dur: 0.32, type:"sine" });""",
 "SETDOWN": """
  S._burst(t, { freq: 440, q: 1.2, gain: 0.10, dur: 0.045, type:"bandpass" });
  S._burst(t + 0.045, { freq: 600, q: 1.8, gain: 0.05, dur: 0.03, type:"bandpass" });
  S._tone (t, { freq: 210, to: 150, gain: 0.06, dur: 0.07, type:"triangle" });
  S._tone (t + 0.08, { freq: 1397, gain: 0.05, dur: 0.44, type:"sine" });
  S._tone (t + 0.08, { freq: 2093, gain: 0.02, dur: 0.30, type:"sine" });""",
 "GLASSBELL": """
  S._burst(t, { freq: 480, q: 1.4, gain: 0.10, dur: 0.05, type:"bandpass" });
  S._tone (t, { freq: 230, to: 160, gain: 0.06, dur: 0.06, type:"triangle" });
  S._tone (t + 0.06, { freq: 1175, gain: 0.05, dur: 0.46, type:"sine" });
  S._tone (t + 0.06, { freq: 2820, gain: 0.022, dur: 0.30, type:"sine" });
  S._tone (t + 0.06, { freq: 5170, gain: 0.010, dur: 0.18, type:"sine" });""",
}
# the staff's own release is `_burst(t, { freq: 380, q: 1.1, gain: 0.055, dur: 0.055, type:"bandpass" })`
LAMP = {
 "BRIGHT": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 760 * k, q: 1.1, gain: 0.04, dur: 0.05, type:"bandpass" });""",
 "BRIGHTER": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 1140 * k, q: 1.4, gain: 0.04, dur: 0.045, type:"bandpass" });""",
 "BRIGHTEST": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 1520 * k, q: 1.6, gain: 0.04, dur: 0.04, type:"bandpass" });""",
 "GLASS": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 760 * k, q: 1.1, gain: 0.035, dur: 0.05, type:"bandpass" });
  S._tone (t, { freq: 1480 * k, gain: 0.012, dur: 0.07, type:"sine" });""",
}
THUMP = {
 "LOWTHUMP": """
  S._tone (t, { freq: 95, to: 55, gain: 0.10, dur: 0.12, type:"sine" });
  S._burst(t, { freq: 160, q: 0.8, gain: 0.05, dur: 0.06, type:"lowpass" });""",
 "DRUM": """
  S._tone (t, { freq: 120, to: 60, gain: 0.10, dur: 0.10, type:"triangle" });""",
 "PUSH": """
  S._burst(t, { freq: 260, q: 0.7, gain: 0.08, dur: 0.09, type:"lowpass" });
  S._tone (t, { freq: 110, to: 62, gain: 0.08, dur: 0.11, type:"triangle" });""",
}


def chime_partials(cast_body: str):
    """The picked cast's chime: every `_tone` in it at a delay (the knock's
    tone is at t and is not chime), as (freq, gain, delay)."""
    out = []
    for m in re.finditer(r"S\._tone \(t \+ ([\d.]+), \{ freq: ([\d.]+)(?:, to: [\d.]+)?, gain: ([\d.]+)", cast_body):
        out.append((float(m.group(2)), float(m.group(3)), float(m.group(1))))
    return out


def reverse_bodies(cast_body: str) -> dict:
    """THE CHIME REVERSED, SHORT: the picked chime's partials as narrow bands of
    noise that swell and cut off (Cipher's construction, v94 build §6).
    SHORT is one swell over 0.30 s; STAGGER2 two swells 0.08 s apart (Cipher's
    single swell was audible for only 0.20 s)."""
    P = chime_partials(cast_body)
    def one(fr, g, t0, dur):
        atk = round(dur * 0.6, 3)
        return f'S._sweep(t + {t0:g}, {{ f0: {fr:g}, f1: {fr:g}, q: 40, gain: {g:g}, dur: {dur}, atk: {atk}, type:"bandpass" }});'
    short = "\n  " + "\n  ".join(one(fr, g, 0, 0.30) for fr, g, _ in P)
    stag = "\n  " + "\n  ".join(one(fr, round(g * k, 5), round(i * 0.08, 3), 0.30)
                                for i, k in enumerate((0.4, 1.0)) for fr, g, _ in P)
    return {"SHORT": short, "STAGGER2": stag}


def pitch(x):
    y = x[int(T0 * SR):int((T0 + 0.1) * SR)]
    sp = np.abs(np.fft.rfft(y * np.hanning(len(y)), n=1 << 16)); ff = np.fft.rfftfreq(1 << 16, 1 / SR)
    m = (ff > 200) & (ff < 6000)
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
        print(f"WATCHLIGHT'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@9.3", ["hit", {"dmg": 9.3}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@9.3"]; H = hit["top"]; rel = C["arrow loose"]
        print("  (hit@9.3 is a wardbolt landing: blade 9.3 x 1.0; 'arrow loose' is the staff's own release)")
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

        # THE CAST, at HIT -6. Rule: audible 0.25-0.50 s ("0.35s"); REG <= 0.6
        # against the shared rune-crack it replaces; PHONE within 12 dB of a
        # hit; it STRIKES -- its top inside the first 0.15 s, the knock or the
        # chime's own strike right behind it, never a swell (round 1 asked 0.10
        # and the chime's strike lands at 0.085-0.105). Of the passers, the
        # audible length nearest 0.35 s.
        R, B, cast = run("THE CAST  -- \"a wooden knock into a glass chime, 0.35s\"", CAST, H - 6,
                         lambda k, m, b: 0.25 <= m["aud"] <= 0.50 and m["topAt"] <= 0.15
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: min(ok, key=lambda k: abs(ok[k]["aud"] - 0.35)),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)

        # THE LANTERN SHOT, level-matched 3 dB under the staff's own release
        # ("quieter: it is the smaller bolt"). Rule: its centroid at least 1.5x
        # the release's ("filtered brighter" -- round 1 asked an octave, 2054 Hz,
        # and the release's own centroid is a noisy 1027); PITCH at n=7 at
        # least 3 semitones over n=1 ("pitched by the lantern's count");
        # audible <= 80 ms; PHONE no more than 4 dB under the release's (the
        # quieter voice may sit under the floor by what it was made quieter
        # by, and no further). Of the passers, the brightest.
        def rise_extra(lo, hi):
            def f(b, m):
                x1 = render(page, [{"at": T0, "body": b, "p": {"n": lo}}], 3.0)
                x2 = render(page, [{"at": T0, "body": b, "p": {"n": hi}}], 3.0)
                return {"rise": 12 * math.log2(pitch(x2) / pitch(x1))}
            return f
        R, B, lamp = run("THE LANTERN SHOT  -- \"the staff's own shot voice, filtered brighter and quieter ... pitched by the count\"",
                         LAMP, rel["top"] - 3,
                         lambda k, m, b: m["cent"] >= 1.5 * rel["cent"] and m["rise"] >= 3 and m["aud"] <= 0.08
                                         and m["phone"] >= floor - 4,
                         lambda ok: max(ok, key=lambda k: ok[k]["cent"]),
                         {"the release": rel}, p={"n": 1}, extra=rise_extra(1, 7))
        keep("lamp", R, B, lamp)

        # THE THUMP, at HIT -8 (under the hit it rides on). Rule: it IS low --
        # at least 30% of it under 150 Hz; audible <= 150 ms; and it must
        # still be HEARD ON A PHONE -- PHONE at least the release's, because a
        # thud that is all under 150 Hz is a thud nobody hears there (the
        # PHONE band, culverin_voice_lab). Of the passers, the loudest on a
        # phone.
        R, B, thump = run("THE THUMP  -- \"a low thump under the hit when knock >= 400\"", THUMP, H - 8,
                          lambda k, m, b: m["low"] >= 0.30 and m["aud"] <= 0.15 and m["phone"] >= floor,
                          lambda ok: max(ok, key=lambda k: ok[k]["phone"]),
                          {"hit": hit})
        keep("thump", R, B, thump)

        # THE CLOSE: "the chime reversed, short" -- the picked chime's own
        # partials, swelling and cut off, at HIT -10. Rule: audible 0.12-0.40 s
        # (short); its TOP in the back half of what is audible (reversed);
        # PHONE within 6 dB of the release. Of the passers, the shortest.
        if out["cast"]["body"]:
            castm = worst(page, body=out["cast"]["body"])[0]
            CL = reverse_bodies(out["cast"]["body"])
            R, B, close = run("THE CLOSE  -- \"the chime reversed, short\"", CL, H - 10,
                              lambda k, m, b: 0.12 <= m["aud"] <= 0.40 and m["topAt"] >= 0.5 * m["aud"]
                                              and m["phone"] >= floor - 6,
                              lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                              {"the cast": castm})
            keep("close", R, B, close)
        keys = ("cast", "lamp", "thump", "close")
        picks = {k: out[k]["body"] for k in keys if k in out}
        if not all(picks.values()) or len(picks) < len(keys):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in keys if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("cast", ["ult", {"w": "watchlight"}], None), ("lamp", ["ult", {"w": "watchlight-lamp", "n": 3}], {"n": 3}),
                                  ("thump", ["ult", {"w": "watchlight-thump"}], None), ("close", ["ult", {"w": "watchlight-close"}], None)]:
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
