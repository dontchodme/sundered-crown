#!/usr/bin/env python
"""CIPHER'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v94.

    python cipher_voice_lab.py --game ../02-chain/sc-converge-blade.html [--json out.json]
    python cipher_voice_lab.py --game ../02-chain/sc-cipher-fx.html --shipped

Design §6.2, every clause:
  the wall-stop "a short stone tap (the bolt has stopped) -- quiet, pitched by
                how many are hanging."
  cast          "a rune-ring 'open' (v75's register, the same school) -- an
                inhale into a chime, 0.4s -- then one soft tap per rune as it
                leaves, in sequence."  (v75 §6.2: "a filtered inhale into a
                soft chime". Oracle is not built on this branch, so the register
                is written here from its words.)
  a hit         "the bow's own arrow voice plus a hex snap." (v75's, the same
                school: "pitch by count".)
  close         "the chime reversed."
The glyph's release is the bow's own (the design names no voice for it).

Rick, 2026-09-27: "you pick i overrule". The method and the measurements are
`culverin_voice_lab.py`'s, imported: offline 48 kHz through `Sfx.buildChain`,
worst of four noise draws, every candidate LEVEL-MATCHED to its voice's target
so the pick is on shape, the PHONE band (>200 Hz) as a floor -- every voice at
least as audible there as the bow's release -- and `--shipped` checking the
built arms against the picked bodies inside the renderer's own floor.

WHERE EACH ONE FIRES (cipher_build stage 6):
  cast   `ult {w:"cipher"}` -- fireUlt, for every relic; Cipher fell through
         to the shared rune-crack until now
  tap    `ult {w:"cipher-tap", n}` -- the wall-stop, n = the caster's sigils
         hanging with this one; it REPLACES the shared "wall" voice for a glyph
         the wall stops (the bolt has stopped, it did not bounce)
  leave  `ult {w:"cipher-leave"}` -- tickConverge, every rune that leaves
  hex    `ult {w:"cipher-hex", n}` -- a sigil's or a flown rune's blow, n = the
         foe's hex stacks after it (hex caps at 5)
  close  `ult {w:"cipher-close"}` -- tickConverge, the window running out by
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
 "INHALE": """
  S._sweep(t, { f0: 500, f1: 2600, q: 0.7, gain: 0.10, dur: 0.32, atk: 0.19, type:"bandpass" });
  S._tone (t + 0.26, { freq: 1318, gain: 0.05, dur: 0.45, type:"sine" });
  S._tone (t + 0.26, { freq: 1976, gain: 0.025, dur: 0.35, type:"sine" });
  S._tone (t + 0.26, { freq: 2637, gain: 0.015, dur: 0.25, type:"sine" });""",
 "EYE": """
  S._sweep(t, { f0: 300, f1: 1800, q: 0.5, gain: 0.11, dur: 0.30, atk: 0.18, type:"lowpass" });
  S._tone (t + 0.24, { freq: 1046, to: 1174, gain: 0.05, dur: 0.40, type:"triangle" });
  S._tone (t + 0.24, { freq: 2093, gain: 0.02, dur: 0.30, type:"sine" });""",
 "BELL": """
  S._sweep(t, { f0: 700, f1: 3000, q: 0.9, gain: 0.09, dur: 0.30, atk: 0.18, type:"bandpass" });
  S._tone (t + 0.25, { freq: 880, gain: 0.05, dur: 0.50, type:"sine" });
  S._tone (t + 0.25, { freq: 2429, gain: 0.02, dur: 0.30, type:"sine" });
  S._tone (t + 0.25, { freq: 4752, gain: 0.01, dur: 0.18, type:"sine" });""",
}
TAP = {
 "STONE": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 1100 * k, q: 3.0, gain: 0.05, dur: 0.025, type:"bandpass" });
  S._tone (t, { freq: 420 * k, to: 260 * k, gain: 0.03, dur: 0.04, type:"triangle" });""",
 "KNOCK": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 700 * k, q: 1.2, gain: 0.05, dur: 0.03, type:"lowpass" });
  S._tone (t, { freq: 520 * k, to: 400 * k, gain: 0.03, dur: 0.05, type:"sine" });""",
 "CHIP": """
  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);
  S._burst(t, { freq: 2400 * k, q: 4.0, gain: 0.04, dur: 0.02, type:"bandpass" });
  S._tone (t, { freq: 960 * k, gain: 0.02, dur: 0.035, type:"sine" });""",
}
LEAVE = {
 "LIFT": """
  S._tone (t, { freq: 1480, to: 2217, gain: 0.03, dur: 0.06, type:"sine" });
  S._burst(t, { freq: 3200, q: 2.0, gain: 0.02, dur: 0.02, type:"bandpass" });""",
 "TICK": """
  S._burst(t, { freq: 2600, q: 5.0, gain: 0.04, dur: 0.025, type:"bandpass" });
  S._tone (t, { freq: 1760, gain: 0.015, dur: 0.03, type:"sine" });""",
 "PLUCK": """
  S._tone (t, { freq: 880, to: 990, gain: 0.035, dur: 0.07, type:"triangle" });""",
}
HEX = {
 "SNAP": """
  const n = Math.max(1, Math.min(5, p.n | 0)), k = Math.pow(2, (n - 1) * 1.5 / 12);
  S._burst(t, { freq: 2800 * k, q: 2.5, gain: 0.06, dur: 0.03, type:"bandpass" });
  S._tone (t, { freq: 1400 * k, to: 700 * k, gain: 0.04, dur: 0.06, type:"square" });""",
 "CRACKLE": """
  const n = Math.max(1, Math.min(5, p.n | 0)), k = Math.pow(2, (n - 1) * 1.5 / 12);
  S._burst(t, { freq: 3400 * k, q: 3.0, gain: 0.05, dur: 0.02, type:"bandpass" });
  S._burst(t + 0.014, { freq: 2200 * k, q: 3.0, gain: 0.05, dur: 0.02, type:"bandpass" });
  S._tone (t, { freq: 660 * k, to: 440 * k, gain: 0.03, dur: 0.05, type:"sawtooth" });""",
 "GLINT": """
  const n = Math.max(1, Math.min(5, p.n | 0)), k = Math.pow(2, (n - 1) * 1.5 / 12);
  S._tone (t, { freq: 1760 * k, to: 1320 * k, gain: 0.04, dur: 0.08, type:"triangle" });
  S._burst(t, { freq: 4000, q: 1.5, gain: 0.03, dur: 0.015, type:"highpass" });""",
}


def chime_partials(cast_body: str):
    """The picked cast's chime: every `_tone` in it, (freq, gain, delay)."""
    out = []
    for m in re.finditer(r"S\._tone \(t(?: \+ ([\d.]+))?, \{ freq: ([\d.]+)(?:, to: [\d.]+)?, gain: ([\d.]+)", cast_body):
        out.append((float(m.group(2)), float(m.group(3)), float(m.group(1) or 0)))
    return out


def reverse_bodies(cast_body: str) -> dict:
    """THE CHIME REVERSED: each partial of the picked chime as a narrow band of
    noise that SWELLS to its peak and cuts off -- a bell played backwards is a
    slow rise and an abrupt end, and `_tone` can only decay (CLAUDE.md 4.5), so
    the rise is `_sweep`'s attack, held on one frequency (f0 = f1) at q 40.
    REVERSE is one swell a partial at the chime's own length.

    ROUND 2: REVERSE was audible for 0.20 s -- an exponential attack from
    -80 dB spends most of itself under the audible line -- so STAGGER lays
    three swells a partial, 0.10 s apart, at a quarter, a half and all of the
    gain: the rise is heard for longer and the last one cuts it off.
    STAGGER_LONG spaces them 0.14 s."""
    P = chime_partials(cast_body)
    def one(fr, g, t0, dur):
        atk = round(dur * 0.6, 3)
        return f'S._sweep(t + {t0:g}, {{ f0: {fr:g}, f1: {fr:g}, q: 40, gain: {g:g}, dur: {dur}, atk: {atk}, type:"bandpass" }});'
    def f(dur):
        return "\n  " + "\n  ".join(one(fr, g, 0, dur) for fr, g, _ in P)
    def stag(gap, dur):
        return "\n  " + "\n  ".join(one(fr, round(g * k, 5), round(i * gap, 3), dur)
                                     for i, k in enumerate((0.25, 0.5, 1.0)) for fr, g, _ in P)
    return {"REVERSE": f(0.45), "STAGGER": stag(0.10, 0.40), "STAGGER_LONG": stag(0.14, 0.45)}


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
        print(f"CIPHER'S VOICES -- {a.game} -- Chromium {ver} -- the method of culverin_voice_lab\n")
        C = {}
        for name, play in [("hit@8.9", ["hit", {"dmg": 8.875}]), ("arrow loose", ["loose", {}]), ("wall", ["wall", {}]),
                           ("rune-crack", ["ult", {"w": "no-arm-control"}])]:
            C[name] = worst(page, play=play)[0]
            print(f"  control  {name:<12} {fmt(C[name])}")
        hit = C["hit@8.9"]; H = hit["top"]
        print("  (hit@8.9 is a glyph, a sigil or a rune landing: blade 8.875 x 1.0 -- every blow this relic lands)")
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

        floor = C["arrow loose"]["phone"]

        def rise_extra(lo, hi):
            def f(b, m):
                x1 = render(page, [{"at": T0, "body": b, "p": {"n": lo}}], 3.0)
                x2 = render(page, [{"at": T0, "body": b, "p": {"n": hi}}], 3.0)
                return {"rise": 12 * math.log2(pitch(x2) / pitch(x1))}
            return f

        # THE CAST, at HIT -6. Rule: audible 0.30-0.60 s ("0.4s"); its TOP at
        # least 0.15 s in (the inhale swells INTO the chime, so the loudest
        # moment is the chime, not the onset); REG <= 0.6 against the shared
        # rune-crack it replaces; PHONE within 12 dB of a hit. Of the passers,
        # the TOP nearest 0.30 s -- an inhale of about three tenths, then the
        # chime, which is the design's 0.4s read literally.
        R, B, cast = run("THE CAST  -- \"an inhale into a chime, 0.4s\"", CAST, H - 6,
                         lambda k, m, b: 0.30 <= m["aud"] <= 0.60 and m["topAt"] >= 0.15
                                         and reg(m, C["rune-crack"]) <= 0.6 and m["phone"] >= hit["phone"] - 12,
                         lambda ok: min(ok, key=lambda k: abs(ok[k]["topAt"] - 0.30)),
                         {"rune-crack": C["rune-crack"]})
        keep("cast", R, B, cast)
        # THE WALL-STOP, at HIT -18 (about two a second across a fight, so
        # quiet). Rule: audible <= 80 ms (a tap); PITCH at n=6 at least 3
        # semitones over n=1 ("pitched by how many are hanging"); PHONE at
        # least the bow's release; REG against the shared "wall" <= 0.9 -- it
        # replaces that voice for a glyph that STOPS, so it must not be that
        # voice. Of the passers, the largest rise -- the count is what the
        # pitch is for.
        R, B, tap = run("THE WALL-STOP  -- \"a short stone tap ... quiet, pitched by how many are hanging\"", TAP, H - 18,
                        lambda k, m, b: m["aud"] <= 0.08 and m["rise"] >= 3 and m["phone"] >= floor
                                        and reg(m, C["wall"]) <= 0.9,
                        lambda ok: max(ok, key=lambda k: ok[k]["rise"]),
                        {"wall": C["wall"]}, p={"n": 1}, extra=rise_extra(1, 6))
        keep("tap", R, B, tap)
        tapm = worst(page, body=out["tap"]["body"], p={"n": 3})[0] if out["tap"]["body"] else None
        # THE LEAVE, at HIT -14 (one per rune, 0.25 s apart at a cast). Rule:
        # audible <= 100 ms, so a sequence 0.25 s apart stays a sequence; PHONE
        # at least the bow's release; REG against the picked wall-stop <= 0.9
        # -- a rune LEAVING must not sound like a rune landing. Of the passers,
        # the one least like the wall-stop.
        R, B, leave = run("THE LEAVE  -- \"one soft tap per rune as it leaves, in sequence\"", LEAVE, H - 14,
                          lambda k, m, b: m["aud"] <= 0.10 and m["phone"] >= floor
                                          and (tapm is None or reg(m, tapm) <= 0.9),
                          lambda ok: min(ok, key=lambda k: reg(ok[k], tapm) if tapm else 0),
                          {"the tap": tapm} if tapm else {})
        keep("leave", R, B, leave)
        # THE HEX SNAP, at HIT -10 (it rides on the arrow's own hit). Rule:
        # audible <= 120 ms; PITCH at n=5 at least 3 semitones over n=2 (a
        # rune's blow is hex 2, so a count starts at 2; v75: "pitch by
        # count"); PHONE at least the bow's release. Of the passers, the one
        # least like the hit it rides on -- it has to be heard OVER it.
        R, B, hexp = run("THE HEX SNAP  -- \"the bow's own arrow voice plus a hex snap\"", HEX, H - 10,
                         lambda k, m, b: m["aud"] <= 0.12 and m["rise"] >= 3 and m["phone"] >= floor,
                         lambda ok: min(ok, key=lambda k: reg(ok[k], hit)),
                         {"hit": hit}, p={"n": 2}, extra=rise_extra(2, 5))
        keep("hex", R, B, hexp)
        # THE CLOSE: "the chime reversed" -- the picked cast's own partials,
        # swelling and cut off, at HIT -8 (under the cast). Rule: audible
        # 0.30-0.65 s; its TOP in the back half of what is audible (reversed:
        # the loudest moment is at the END); PHONE within 6 dB of the release.
        # Of the passers, the shortest (the chime's own length is the model).
        if out["cast"]["body"]:
            castm = worst(page, body=out["cast"]["body"])[0]
            CL = reverse_bodies(out["cast"]["body"])
            R, B, close = run("THE CLOSE  -- \"the chime reversed\"", CL, H - 8,
                              lambda k, m, b: 0.30 <= m["aud"] <= 0.65 and m["topAt"] >= 0.5 * m["aud"]
                                              and m["phone"] >= floor - 6,
                              lambda ok: min(ok, key=lambda k: ok[k]["aud"]),
                              {"the cast": castm})
            keep("close", R, B, close)
        keys = ("cast", "tap", "leave", "hex", "close")
        picks = {k: out[k]["body"] for k in keys if k in out}
        if not all(picks.values()) or len(picks) < len(keys):
            raise SystemExit("a voice has no pick: " + ", ".join(k for k in keys if not picks.get(k)))
        out["bodies"] = picks
        print("\nTHE PICKS: " + ", ".join(f"{k} {out[k]['pick']}" for k in picks))
        if a.shipped:
            print("\nTHE SHIPPED ARMS against the picked bodies:")
            bad = 0
            for key, play, pp in [("cast", ["ult", {"w": "cipher"}], None), ("tap", ["ult", {"w": "cipher-tap", "n": 3}], {"n": 3}),
                                  ("leave", ["ult", {"w": "cipher-leave"}], None), ("hex", ["ult", {"w": "cipher-hex", "n": 4}], {"n": 4}),
                                  ("close", ["ult", {"w": "cipher-close"}], None)]:
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
