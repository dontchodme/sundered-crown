"""A SCRATCH BUILD ON THE LAB'S CLOCK (v112 §2, control 2): a copy of a built link in which `tickRootfast`
is ALSO called on every frozen step -- the hit stop, the latch and the split hold -- so the window runs
through freezes as the lab's `castEnd` did (8 step-seconds of match time). Nothing else changes; the
charge stays on the engine's clock (the lab's 15 is the engine's 13 by the census).
    python clock_variant.py <link.html> <out.html>"""
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old)
    return s.replace(old, new, 1)
TAG = "      this.tickRootfast(dt);   // CLOCK VARIANT: the window runs through the freeze (the lab's clock)\n"
src = one(src, "      L.t += dt;\n      this.t += dt;\n", "      L.t += dt;\n      this.t += dt;\n" + TAG)
src = one(src, "      S.t += dt;\n      this.t += dt;\n", "      S.t += dt;\n      this.t += dt;\n" + TAG)
src = one(src, "      this.hitStop -= dt;\n      this.t += dt;\n", "      this.hitStop -= dt;\n      this.t += dt;\n" + TAG)
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8", newline="\n")
print(pathlib.Path(sys.argv[2]).name, hashlib.sha256(src.encode()).hexdigest()[:16])
