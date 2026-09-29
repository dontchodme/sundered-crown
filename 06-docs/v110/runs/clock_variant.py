"""Scratch control for v110 §2 (v108's clock_variant.py, for the halo): a built halo link with
its clock moved onto the LAB's clock -- `tickHalo` ALSO runs on every frozen step (the latch,
the split hold and the hit stop), so the window and both cooldowns run through freezes, as the
lab's onFrame did. Written to scratch only; never a link.
    python clock_variant.py <src link> <out>"""
import pathlib, sys, hashlib
src, out = sys.argv[1], sys.argv[2]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(s, a, b):
    assert s.count(a) == 1, a
    return s.replace(a, b, 1)
s = one(s, "      if (L.t >= L.dur) this.blast(L);\n", "      this.tickHalo(dt);   // CONTROL: the lab's clock\n      if (L.t >= L.dur) this.blast(L);\n")
s = one(s, "      if (S.t >= S.dur) this.releaseSplit();\n", "      this.tickHalo(dt);   // CONTROL: the lab's clock\n      if (S.t >= S.dur) this.releaseSplit();\n")
s = one(s, "      this.hitStop -= dt;\n", "      this.hitStop -= dt;\n      this.tickHalo(dt);   // CONTROL: the lab's clock\n")
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(out, hashlib.sha256(s.encode()).hexdigest()[:16])
