# Scratch copies of tools/overlays/rootfast.js (the design's lab), each changing one thing, none moving a fight
# unless named:
#   rootfast_trans.js  COUNTS the lab's roots as TRANSITIONS too (S.trans: a blow that finds the foe unpinned),
#                      the brief's "roots a cast counted as transitions"; fights identical to rootfast.js
import pathlib
src = pathlib.Path("C:/dev/sundered-crown/tools/overlays/rootfast.js").read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new, 1)
t = one(src, "if (foe.alive){ H.pin(foe, rootFor);",
        "if (foe.alive){ if (!(foe.pin > 0)) S.trans = (S.trans || 0) + 1; H.pin(foe, rootFor);")
pathlib.Path(__file__).with_name("rootfast_trans.js").write_text(t, encoding="utf-8", newline="\n")
print("ok")
