#!/usr/bin/env python3
"""DOES THE ANNOUNCER LAND ON THE IGNITIONS -- FOR EVERY RELIC, NOT ONE PAIR?

    python vo_sync_probe.py
    python vo_sync_probe.py --names Ironhail,Goreshard

Since 2026-08-29 the shipped line is placed on the opening's own flares:

    <A>,        at flareA    0.10s
    <B>.        at flareB    0.95s
    Who wins?   on the pull  1.95s

Those onsets come out of `src/render/open.js`; the NAMES come out of Kokoro,
and they are not all the same length. The stagger between the two flares is
0.85s and a name longer than that pushes the next part late -- `cinema_vo.py`
never overlaps, it delays and prints the drift.

**A clip renders one pairing and this ships for all 300.** So the ceiling gets
measured across the roster rather than assumed off the pair that happened to be
filmed, which is the same mistake `ignition_probe.py` check 3 made and had to
be rewritten for.

The arithmetic is small and worth stating, because it means 50 renders and not
600: the second name's drift depends only on the FIRST name's length, and the
question's drift depends only on the second name's. No pair needs rendering.

REQUIRES THE KOKORO MODEL (353 MB, not in the repo -- tools/FETCH-KOKORO.md).
Nothing else in the ignition work does, which is why this is its own file and
not another check inside `ignition_probe.py`.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import cinema_vo

HERE = pathlib.Path(__file__).resolve().parent


def spoken_len(k, np, text, voice, lang):
    sm, sr = k.create(cinema_vo.normalise(text), voice=voice,
                      speed=cinema_vo.SPEED, lang=lang)
    sm = np.asarray(sm, dtype="float32")
    loud = np.where(abs(sm) > 0.012)[0]
    if len(loud):
        sm = sm[max(0, loud[0] - int(sr * 0.03)):
                min(len(sm), loud[-1] + int(sr * 0.06))]
    return len(sm) / sr


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--names", default=None,
                    help="comma-separated display names; default is the roster "
                         "read out of the build")
    ap.add_argument("--voice", default=cinema_vo.VOICE)
    ap.add_argument("--tolerance", type=float, default=0.20,
                    help="seconds of drift that still reads as on the beat. "
                         "0.20 is twelve frames at 60fps and is the bar this "
                         "shipped against -- state it, do not tune it to pass.")
    A = ap.parse_args()

    fa, fb, fq = cinema_vo.ignition_beats()
    stagger = fb - fa
    print(f"the opening's beats, from src/render/open.js:")
    print(f"  flareA {fa:.2f}s   flareB {fb:.2f}s   the pull {fq:.2f}s"
          f"   stagger {stagger:.2f}s\n")

    if A.names:
        names = [n.strip() for n in A.names.split(",") if n.strip()]
    else:
        from scpage import game
        with game(game_path=(HERE / A.game).resolve()) as (page, errors):
            names = page.evaluate("() => AC.WEAPONS.map(w => w.name)")
        print(f"roster: {len(names)} relics out of {A.game}\n")

    for p in (cinema_vo.MODEL, cinema_vo.VOICES):
        if not p.exists():
            print(f"! missing {p.name} -- see tools/FETCH-KOKORO.md")
            return 2
    from kokoro_onnx import Kokoro
    import numpy as np
    k = Kokoro(str(cinema_vo.MODEL), str(cinema_vo.VOICES))
    lang = "en-us" if A.voice.startswith("a") else "en-gb"

    # As relic A the name is rendered "Name,"; as relic B it is "Name." Both
    # are measured because the two forms differ and both feed a different drift.
    rows = []
    for n in names:
        la = spoken_len(k, np, f"{n},", A.voice, lang)
        lb = spoken_len(k, np, f"{n}.", A.voice, lang)
        rows.append((n, la, lb))
        print(f"  {n:<14} as A {la:.2f}s   as B {lb:.2f}s")

    # B starts at max(flareB, flareA + lenA). The question starts at
    # max(pull, B's end).
    b_drift = [(n, max(0.0, (fa + la) - fb)) for n, la, _ in rows]
    worst_b = max(b_drift, key=lambda r: r[1])
    late_b = [r for r in b_drift if r[1] > 0.005]

    # the question's worst case is the longest B behind the longest A
    longest_a = max(la for _, la, _ in rows)
    q_drift = [(n, max(0.0, max(fb, fa + longest_a) + lb - fq))
               for n, _, lb in rows]
    worst_q = max(q_drift, key=lambda r: r[1])

    print(f"\nSECOND NAME, off its flare by:")
    print(f"  {len(late_b)}/{len(rows)} first names overrun the {stagger:.2f}s "
          f"stagger")
    print(f"  worst {worst_b[1]:.2f}s, after {worst_b[0]}"
          f"   ({worst_b[1] * 60:.0f} frames at 60fps)")
    print(f"THE QUESTION, off the pull by:")
    print(f"  worst {worst_q[1]:.2f}s, {worst_q[0]} behind the longest first "
          f"name ({longest_a:.2f}s)")

    ok = worst_b[1] <= A.tolerance and worst_q[1] <= A.tolerance
    print(f"\n{'PASS' if ok else 'FAIL'}  worst drift "
          f"{max(worst_b[1], worst_q[1]):.2f}s against a stated "
          f"{A.tolerance:.2f}s bar.")
    if not ok:
        print("      The fix is `flareB` in src/render/open.js -- ONE number,")
        print("      and it is a change to a look Rick approved, so it is his.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
