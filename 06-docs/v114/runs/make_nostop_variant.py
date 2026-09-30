"""v114 scratch control (§2): the match-clock variant with fireUlt's common 0.08 cast stop taken off
Goreshard's cast -- the lab's window AND the lab's cast (the lab never froze the world at a cast). One
line more than make_matchclock_variant.py's two. A scratch file, never a link.

    python make_nostop_variant.py <ctl-goreshard-matchclock.html> <out.html>
"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
a = ("    this.shake = 32;   // Mountainfall's 52 moved to the Crucible's strike\n"
     "    this.hitStop = Math.max(this.hitStop, 0.08);\n")
b = ("    this.shake = 32;   // Mountainfall's 52 moved to the Crucible's strike\n"
     "    if (f.w.id !== \"oathwound\") this.hitStop = Math.max(this.hitStop, 0.08);   // SCRATCH VARIANT: no cast stop (the lab's cast)\n")
assert src.count(a) == 1, "the cast stop anchor"
assert "SCRATCH VARIANT: the window on match time" in src, "not the match-clock variant"
src = src.replace(a, b, 1)
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8", newline="\n")
print("written", sys.argv[2])
