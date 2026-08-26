#!/usr/bin/env python3
"""`physics.massRef` HAS DRIFTED. By how much, and what to do about it.
Full rationale in the project doc. Short version: massRef sets which mass falls
at exactly 1x gravity; the shipped 2.7 is the v9 SIX-relic mean on a roster of
nine; a uniform error is not a wrong relic, which is why no check caught it.
Do not edit the constant alone -- assert it, and move it inside a tuner run."""
from __future__ import annotations
import argparse, math, pathlib, re

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sundered-crown-next.html")
    a = ap.parse_args()
    t = (pathlib.Path(__file__).parent / a.game).read_text(encoding="utf-8")
    ref = float(re.search(r"massRef:\s*([0-9.]+)", t).group(1))
    weight = float(re.search(r"massWeight:\s*([0-9.]+)", t).group(1))
    i = t.index("const WEAPONS = [")
    blk = t[i:t.index("\n];", i)]
    relics = [(m.group(1), float(m.group(2))) for m in
              re.finditer(r'id:"([a-z]+)"[\s\S]{0,400}?mass:([0-9.]+)', blk)]
    if not relics: raise SystemExit("no relics parsed")
    masses = [m for _, m in relics]; n = len(masses)
    arith = sum(masses)/n
    neutral = (sum(math.sqrt(m) for m in masses)/n)**2
    mult = [(m/ref)**weight for m in masses]; mean_mult = sum(mult)/n
    print(f"=== physics.massRef — {a.game} ===\n")
    print(f"shipped massRef {ref}   massWeight {weight}   roster {n} relics\n")
    print(f"{'relic':<14}{'mass':>7}{'fall x':>9}")
    for (wid,m),k in sorted(zip(relics,mult), key=lambda z:-z[0][1]):
        print(f"{wid:<14}{m:>7.1f}{k:>9.3f}")
    print(f"\nmean fall multiplier            {mean_mult:.3f}   <-- should be 1.000")
    print(f"the whole roster is falling      {(mean_mult-1)*100:+.1f}% against neutral")
    print(f"\ncandidate massRef values")
    print(f"   arithmetic mean of mass       {arith:.3f}   (the config comment's definition)")
    print(f"   mean(sqrt(mass))^2            {neutral:.3f}   (makes mean multiplier exactly 1)")
    print(f"   shipped                       {ref:.3f}   (the mean of the SIX-relic roster)")
    # An assertion that says FAIL when the constant is RIGHT is worse than no
    # assertion: this printed "would FAIL at 2.68" against a re-derived 2.68
    # on the day the drift was finally closed. State the verdict, not the ask.
    ok = abs(ref - neutral) <= 0.005
    print(f"\n   an assertion wants {neutral:.2f}; shipped is {ref} — "
          f"{'PASS' if ok else 'FAIL'}"
          + ("" if ok else f" (off by {abs(ref-neutral):.3f})") + ".")

main()
