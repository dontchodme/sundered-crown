"""Scratch controls for v108 §2: a built hail link with its clocks moved onto the LAB's clock.
  lab   -- tickHail also runs on every frozen step (hit stop, latch, split): the window, the
           cadence and every bolt's fall run through freezes, as the lab's onFrame did.
  fall  -- only the bolts in the air fall through freezes; the window and the cadence stay on
           the window tickers' clock.
Written to scratch only; never a link."""
import pathlib, sys, hashlib
src, kind, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(s, a, b):
    assert s.count(a) == 1, a
    return s.replace(a, b, 1)
arg = "dt" if kind == "lab" else "dt, true"
s = one(s, "      if (L.t >= L.dur) this.blast(L);\n", f"      this.tickHail({arg});   // CONTROL: the lab's clock\n      if (L.t >= L.dur) this.blast(L);\n")
s = one(s, "      if (S.t >= S.dur) this.releaseSplit();\n", f"      this.tickHail({arg});   // CONTROL: the lab's clock\n      if (S.t >= S.dur) this.releaseSplit();\n")
s = one(s, "      this.hitStop -= dt;\n", f"      this.hitStop -= dt;\n      this.tickHail({arg});   // CONTROL: the lab's clock\n")
if kind == "fall":
    s = one(s, "  tickHail(dt){\n", "  tickHail(dt, frozen){\n")
    s = one(s, "    for (const f of [this.a, this.b]){\n      const Z = f.ultHail;\n", "    if (frozen) return;   // CONTROL: only the fall runs through freezes\n    for (const f of [this.a, this.b]){\n      const Z = f.ultHail;\n")
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(out, hashlib.sha256(s.encode()).hexdigest()[:16])
