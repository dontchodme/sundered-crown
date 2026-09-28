"""CONTROL (v103 §2): a scratch copy of a built Temper link whose window clock runs
THROUGH freezes, as the lab's did -- ultTemper.t also advances on the three frozen
paths of `step` (hit stop, latch, split hold). Nothing else changes. Not a link."""
import sys, pathlib, hashlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = src.read_text(encoding="utf-8")
INC = "\n      for (const f of [this.a, this.b]) if (f.ultTemper) f.ultTemper.t += dt;   // CONTROL: the lab's clock"
for a in ("      this.hitStop -= dt;\n      this.t += dt;", "      L.t += dt;\n      this.t += dt;", "      S.t += dt;\n      this.t += dt;"):
    assert s.count(a) == 1, a
    s = s.replace(a, a + INC)
out.write_text(s, encoding="utf-8", newline="\n")
print(out.name, hashlib.sha256(s.encode()).hexdigest()[:16])
