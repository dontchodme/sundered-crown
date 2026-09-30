"""A SCRATCH BUILD ON THE LAB'S CLOCK (v113 §2, control 2): a copy of a built link in which `tickBramble`
is ALSO called on every frozen step -- the hit stop, the latch and the split hold -- so the window, the
brambles' lives and the thorns' cooldown all run through freezes, and the thorns test, snare and bite on
frozen steps, as the lab's `onFrame` did (it ran after every `m.step`, frozen or not). Nothing else
changes; the charge stays on the engine's clock (the lab's 16 is the engine's 14 by the census).
    python clock_variant.py <link.html> <out.html>"""
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old)
    return s.replace(old, new, 1)
TAG = "      this.tickBramble(dt);   // CLOCK VARIANT: the brambles run through the freeze (the lab's clock)\n"
src = one(src, "      L.t += dt;\n      this.t += dt;\n", "      L.t += dt;\n      this.t += dt;\n" + TAG)
src = one(src, "      S.t += dt;\n      this.t += dt;\n", "      S.t += dt;\n      this.t += dt;\n" + TAG)
src = one(src, "      this.hitStop -= dt;\n      this.t += dt;\n", "      this.hitStop -= dt;\n      this.t += dt;\n" + TAG)
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8", newline="\n")
print(pathlib.Path(sys.argv[2]).name, hashlib.sha256(src.encode()).hexdigest()[:16])
