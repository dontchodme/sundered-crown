"""SCRATCH CONTROLS for v107 (never links of the chain). Each takes a built Bulwark link and changes ONE thing.
    python ctl_variant.py SRC OUT KIND
KIND:
  labclock   the wall's clock runs through freezes, as the lab's did: tickLightwall is also called on
             every frozen step (hit stop, latch, split hold), so the window, the cooldown and the tests
             run on step-seconds.
"""
import sys, pathlib, re, hashlib
src, out, kind = sys.argv[1], sys.argv[2], sys.argv[3]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new, 1)
if kind == "labclock":
    one("      this.decayImpactOnly(dt);\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.",
        "      this.decayImpactOnly(dt);\n      this.tickLightwall(dt);   // CONTROL: the lab's clock\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.")
    one("      if (L.t >= L.dur) this.blast(L);\n      return;",
        "      if (L.t >= L.dur) this.blast(L);\n      this.tickLightwall(dt);   // CONTROL: the lab's clock\n      return;")
    one("      if (S.t >= S.dur) this.releaseSplit();\n      return;",
        "      if (S.t >= S.dur) this.releaseSplit();\n      this.tickLightwall(dt);   // CONTROL: the lab's clock\n      return;")
else:
    raise SystemExit("unknown kind")
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(kind, pathlib.Path(out).name, hashlib.sha256(s.encode()).hexdigest()[:16])
