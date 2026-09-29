#!/usr/bin/env python
"""SCRATCH CONTROLS for v104 §2 (never on the chain):
  matchclock  the rise's window clock also runs through every frozen step (hit
              stop, latch, split hold) -- the lab's clock, where 8s is 8s of match
  rise0       the rise at 0s: lit on the cast frame, the caster put at the hang
              point at once -- the lab's teleport
Usage: make_variant.py <link> <out> matchclock|rise0 [...]"""
import sys, hashlib, pathlib
src, out, *kinds = sys.argv[1:]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:60])
    return s.replace(old, new, 1)
ADV = " for (const q of [this.a, this.b]) if (q.ultRise) q.ultRise.t += dt;   /* CTL matchclock */"
for k in kinds:
    if k == "matchclock":
        s = one(s, "      this.hitStop -= dt;\n      this.t += dt;\n", "      this.hitStop -= dt;\n      this.t += dt;" + ADV + "\n")
        s = one(s, "      L.t += dt;\n      this.t += dt;\n", "      L.t += dt;\n      this.t += dt;" + ADV + "\n")
        s = one(s, "    if (this.splitHold){\n      const S = this.splitHold;\n      S.t += dt;\n      this.t += dt;\n",
                "    if (this.splitHold){\n      const S = this.splitHold;\n      S.t += dt;\n      this.t += dt;" + ADV + "\n")
    elif k == "rise0":
        s = one(s, "rise:0.35, hangY:300,", "rise:0, hangY:300,")
    else:
        raise SystemExit(k)
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(out, hashlib.sha256(s.encode()).hexdigest()[:16], kinds)
