#!/usr/bin/env python
"""CROZIER'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v95.

    python crozier_voice_lab.py --game ../02-chain/sc-radiance-blade.html [--json out.json]
    python crozier_voice_lab.py --game ../02-chain/sc-crozier-fx.html --shipped

Design §6.2, every clause:
  the spell   "a very short bright tick (the needle), pitched high; on a pierce
              the same tick with a glassy after-ring."
  cast        "a rising choir swell, 0.4s (the school's register: Zenith,
              Daybreak)."
  a grown     "the hit voice with a low bloom under it that scales with `k`."
  landing
  close       "the swell reversed."

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target
so the pick is on shape, the PHONE band (>200 Hz) as a floor, and `--shipped`
checking the built arms against the picked bodies inside the renderer's own
floor.

WHERE EACH ONE FIRES (crozier_build stage 6):
  tick    `loose {spell:"lance"}` -- spawnShot, every lance, in the loose voice's
          own branch (Culverin's slug is the precedent)
  pierce  `ult {w:"crozier-pierce"}` -- tickShots, a lance entering a foe
          blade's reach (it goes through; the flick is drawn there too)
  cast    `ult {w:"crozier"}` -- fireUlt; Crozier fell through to the rune-crack
  bloom   `ult {w:"crozier-bloom", k}` -- the hit branch, after the hit voice,
          a GROWN lance landing, k its growth (0-1)
  close   `ult {w:"crozier-close"}` -- tickRadiance, the window running out by
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

TICK = {
 "NEEDLE": """
  S._burst(t, { freq: 5200, q: 3.0, gain: 0.05, dur: 0.015, type:"bandpass" });
  S._tone (t, { freq: 3136, gain: 0.02, dur: 0.03, type:"sine" });""",
 "PING": """
  S._tone (t, { freq: 2637, to: 2960, gain: 0.03, dur: 0.035, type:"sine" });""",
 "CLICK": """
  S._burst(t, { freq: 4200, q: 1.2, gain: 0.05, dur: 0.012, type:"highpass" });""",
}
def chord(fs, gs, lo, q, breath=None):
    """A choir swell as LITERAL lines, one `_sweep` a partial a swell -- two
    staggered swells, the first at 0.4. Round 2 wrote the gains as `k * [...]`,
    which `scale_gains` cannot see: the level match rescaled only the breath
    layer, and HALO (no breath) could not be matched at all (-35 against -25)."""
    out = []
    for d, k in ((0, 0.4), (0.12, 1.0)):
        for f, g in zip(fs, gs):
            out.append(f'S._sweep(t + {d:g}, {{ f0: {round(f * lo, 1):g}, f1: {f}, q: {q}, gain: {round(g * k, 4):g}, dur: 0.46, atk: 0.27, type:"bandpass" }});')
    if breath:
        out.append(f'S._sweep(t + 0.1, {{ f0: {breath[0]}, f1: {breath[1]}, q: 0.8, gain: 0.03, dur: 0.46, atk: 0.27, type:"bandpass" }});')
    return "\n  " + "\n  ".join(out)


CAST = {
 # ROUND 3 (round 2 in runs/build/stage6_voice_lab_round2.txt): the same three
 # chords with every gain a literal, so the level match can reach them.
 "CHOIR": chord([523, 659, 784], [0.30, 0.22, 0.18], 0.89, 24, (900, 2600)),
 "HALO": chord([1047, 1319, 1568], [0.30, 0.22, 0.18], 0.89, 30),
 "FIFTHS": chord([392, 587, 784], [0.32, 0.24, 0.18], 0.84, 22, (700, 2200)),
}
BLOOM = {
 # ROUND 2: round 1's `0.02 + 0.08 k` spans 9 dB from k 0.2 to 1; the gain is
 # proportional to k now (14 dB), and SWELL's tone sits low enough to be low.
 "SWELL": """
  const k = Math.max(0, Math.min(1, p.k === undefined ? 1 : p.k));
  S._tone (t, { freq: 120, to: 60, gain: 0.10 * k, dur: 0.16, type:"triangle" });
  S._burst(t, { freq: 300, q: 0.8, gain: 0.04 * k, dur: 0.08, type:"lowpass" });""",
 "BODY": """
  const k = Math.max(0, Math.min(1, p.k === undefined ? 1 : p.k));
  S._tone (t, { freq: 110, to: 60, gain: 0.10 * k, dur: 0.14, type:"triangle" });""",
 "WARM": """
  const k = Math.max(0, Math.min(1, p.k === undefined ? 1 : p.k));
  S._sweep(t, { f0: 500, f1: 180, q: 0.9, gain: 0.10 * k, dur: 0.18, atk: 0.03, type:"lowpass" });
  S._tone (t, { freq: 130, to: 75, gain: 0.06 * k, dur: 0.15, type:"sine" });""",
}


def pierce_bodies(tick_body: str) -> dict:
    """ON A PIERCE: the picked tick with a glassy after-ring -- two high sine
    partials ringing ~0.2s (RING) or ~0.3s (RING_LONG) under it."""
    def f(dur):
        return (tick_body + f"""
  S._tone (t + 0.008, {{ freq: 2637, gain: 0.018, dur: {dur}, type:"sine" }});
  S._tone (t + 0.008, {{ freq: 3951, gain: 0.010, dur: {round(dur * 0.7, 3)}, type:"sine" }});""")
    return {"RING": f(0.22), "RING_LONG": f(0.32)}


def close_bodies(cast_body: str) -> dict:
    """THE SWELL REVERSED: the cast swelled up INTO its chord; the close starts
    on the chord and falls away from it -- the chord's partials (the full swell,
    the one at +0.12) as `_tone`s, whose exponential ramp is exactly a swell
    played backwards, gliding DOWN by the ratio the cast rose by. FALL at the
    cast's length, FALL_SHORT shorter."""
    import re as _re
    rows = [(float(m.group(2)), float(m.group(1))) for m in _re.finditer(
        r"S\._sweep\(t \+ 0\.12, \{ f0: ([\d.]+), f1: ([\d.]+), q:", cast_body)]
    def f(dur):
        return "\n  " + "\n  ".join(
            f'S._tone (t, {{ freq: {f1:g}, to: {f0:g}, gain: {g}, dur: {dur}, type:"sine" }});'
            for (f1, f0), g in zip(rows, (0.05, 0.035, 0.028)))
    return {"FALL": f(0.42), "FALL_SHORT": f(0.30)}


def pitch(x):
    y = x[int(T0 * SR):int((T0 + 0.1) * SR)]
    sp = np.abs(np.fft.rfft(y * np.hanning(len(y)), n=1 << 16)); ff = np.fft.rfftfreq(1 << 16, 1 / SR)
    m = (ff > 200) & (ff < 12000)
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
        print(f"CROZIER'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@12.8", ["hit", {"dmg": 12.75}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@12.8"]; H = hit["top"]; rel = C["arrow loose"]
        print("  (hit@12.8 is a lance landing: blade 12.75 x 1.0; 'arrow loose' is the staff's generic release)")
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

        # THE TICK, level-matched to the staff's own release (a loose voice sits
        # UNDER the impacts: the generic release's own comment). Rule: audible
        # <= 40 ms ("very short"); its centroid 2.5-6 kHz ("bright ... pitched
        # high" -- round 1 took a 12.5 kHz CLICK, a hiss with no pitch at all);
        # PHONE at least the release's. Of the passers, the shortest.
        R, B, tick = run("THE TICK  -- \"a very short bright tick (the needle), pitched high\"", TICK, rel["top"],
                         lambda k, m, b: m["aud"] <= 0.04 and 2500 <= m["cent"] <= 6000 and m["phone"] >= floor - 0.5,
                         lambda ok: min(ok, key=lambda k: (ok[k]["aud"], -ok[k]["cent"])),
                         {"the release": rel})
        keep("tick", R, B, tick)

        # ON A PIERCE: the picked tick with a glassy after-ring, at the tick's
        # level + 3 dB (it is the tick AND a ring). Rule: audible 0.12-0.35 s
        # (a ring, not a tick); the after-ring GLASSY -- centroid 2-4 kHz;
        # PHONE at least the release's. "The same tick" holds by construction
        # (the body IS the tick's lines, then the ring): round 3 dropped a REG
        # against the tick, because a whole-sound spectrum is the 0.2s ring's
        # and a 30 ms onset cannot move it (0.06 on both). Of the passers, the
        # shorter.
        if out["tick"]["body"]:
            tickm = worst(page, body=out["tick"]["body"])[0]
            R, B, pierce = run("ON A PIERCE  -- \"the same tick with a glassy after-ring\"", pierce_bodies(out["tick"]["body"]),
                               rel["top"] + 3,
                               lambda k, m, b: 0.12 <= m["aud"] <= 0.35 and 2000 <= m["cent"] <= 4000 and m["phone"] >= floor,
                               lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                               {"the tick": tickm})
            keep("pierce", R, B, pierce)

        # THE CAST, at HIT -6. Rule: audible 0.30-0.55 s ("0.4s"); it SWELLS --
        # its top at least 60% of the way through what is audible ("rising");
        # REG <= 0.6 against the rune-crack it replaces; PHONE within 12 dB of a
        # hit. Of the passers, the audible length nearest 0.4 s. (Round 1 asked
        # the top at 60%; a swell's is 55-60% of the way through what is heard.)
        R, B, cast = run("THE CAST  -- \"a rising choir swell, 0.4s\"", CAST, H - 6,
                         lambda k, m, b: 0.30 <= m["aud"] <= 0.55 and m["topAt"] >= 0.55 * m["aud"]
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: min(ok, key=lambda k: abs(ok[k]["aud"] - 0.4)),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)

        # THE BLOOM, at HIT -8 at k = 1 (under the hit it rides on). Rule: it IS
        # low -- at least 30% under 150 Hz; audible <= 0.20 s; HEARD ON A PHONE
        # at k = 1 (PHONE at least the release's); and it SCALES WITH k -- at
        # least 12 dB quieter at k = 0.2 than at k = 1. Of the passers, the
        # loudest on a phone.
        def k_extra(b, m):
            lo = worst(page, body=b, p={"k": 0.2})[0]
            return {"k02": m["top"] - lo["top"]}
        R, B, bloom = run("THE BLOOM  -- \"a low bloom under the hit that scales with k\"", BLOOM, H - 8,
                          lambda k, m, b: m["low"] >= 0.30 and m["aud"] <= 0.20 and m["phone"] >= floor and m["k02"] >= 12,
                          lambda ok: max(ok, key=lambda k: ok[k]["phone"]),
                          {"hit": hit}, p={"k": 1}, extra=k_extra)
        keep("bloom", R, B, bloom)

        # THE CLOSE: "the swell reversed" -- the picked chord falling away, at
        # HIT -8. Rule: audible 0.20-0.50 s; its top in the FIRST 30% of what is
        # audible (the swell's top was at its end); PHONE within 6 dB of the
        # release. Of the passers, the length nearest the cast's.
        if out["cast"]["body"]:
            castm = worst(page, body=out["cast"]["body"])[0]
            R, B, close = run("THE CLOSE  -- \"the swell reversed\"", close_bodies(out["cast"]["body"]), H - 8,
                              lambda k, m, b: 0.20 <= m["aud"] <= 0.50 and m["topAt"] <= 0.3 * m["aud"] and m["phone"] >= floor - 6,
                              lambda ok: min(ok, key=lambda k: abs(ok[k]["aud"] - castm["aud"])),
                              {"the cast": castm})
            keep("close", R, B, close)
        keys = ("tick", "pierce", "cast", "bloom", "close")
        picks = {k: out[k]["body"] for k in keys if k in out}
        if not all(picks.values()) or len(picks) < len(keys):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in keys if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("tick", ["loose", {"spell": "lance"}], None), ("pierce", ["ult", {"w": "crozier-pierce"}], None),
                                  ("cast", ["ult", {"w": "crozier"}], None), ("bloom", ["ult", {"w": "crozier-bloom", "k": 0.7}], {"k": 0.7}),
                                  ("close", ["ult", {"w": "crozier-close"}], None)]:
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
