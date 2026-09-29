#!/usr/bin/env python
"""SCRATCH MUTANTS of the stage-6 Angelus link (v104 §5e). Each breaks one
stage-6 sentence; each must fail its own stage-6 check ([11] or [12]) and no
other. Usage: make_mutants6.py <fx link> <out dir>"""
import sys, hashlib, pathlib
src, outd = sys.argv[1], pathlib.Path(sys.argv[2])
s0 = pathlib.Path(src).read_text(encoding="utf-8")


def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:70])
    return s.replace(old, new, 1)


M = {
  # [11] "the chord resolving down" only on a close BY THE CLOCK with both
  # alive (reading 15): here it plays on every close, a death's included.
  # Voices only: no fight moves.
  "m9-chorddeath": [("        if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){\n"
                     "          SFX.play(\"ult\", { w: \"angelus-close\" });",
                     "        if (Z.t >= Z.dur || !f.alive){\n"
                     "          SFX.play(\"ult\", { w: \"angelus-close\" });")],
  # [12] "the picture closes it" at the kill (reading 10; Canopy's rule): here
  # the picture reads the window without `over`, so a window the sim leaves open
  # at the kill keeps its shafts and halo up through the verdict. Presentation
  # only: no fight moves.
  "m10-overopen": [("      const Z = (this.over || !f.alive) ? null : f.ultRise;\n      if (Z){\n"
                    "        if (!(f.ascendFade > 0) || f.ascendOut > 0){            // a cast",
                    "      const Z = !f.alive ? null : f.ultRise;\n      if (Z){\n"
                    "        if (!(f.ascendFade > 0) || f.ascendOut > 0){            // a cast")],
  # [12] "nothing in the simulation reads any of it": here the picture's heal
  # flare nudges the foe (1e-9 on its vx) -- a picture that writes the sim.
  "m11-picwrite": [("        f.ascendHeal = 0;                                       // the halo flares\n",
                    "        f.ascendHeal = 0;                                       // the halo flares\n"
                    "        (f === this.a ? this.b : this.a).vx += 1e-9;            /* MUTANT m11-picwrite */\n")],
  # [11] "the ball's landing thud" only on the first floor contact after a
  # clock close (reading 18): here every floor contact of a caster that has
  # cast thuds. Voices only: no fight moves.
  "m12-thudall": [("      if (f.riseTally && f.riseTally.falling && f.alive && f.y >= hiY){",
                   "      if (f.riseTally && f.alive && f.y >= hiY){")],
}
outd.mkdir(parents=True, exist_ok=True)
for k, eds in M.items():
    s = s0
    for o, n in eds:
        s = one(s, o, n)
    p = outd / f"sc-angelus-{k}.html"
    if p.exists():
        if p.read_text(encoding="utf-8") != s:
            raise SystemExit(f"refusing to overwrite {p}: it is not this mutant")
        print(p.name, hashlib.sha256(s.encode()).hexdigest()[:16], "(already made: the same bytes)")
        continue
    p.write_text(s, encoding="utf-8", newline="\n")
    print(p.name, hashlib.sha256(s.encode()).hexdigest()[:16])
