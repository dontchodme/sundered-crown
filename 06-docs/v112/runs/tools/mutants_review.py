"""v112 §3: THE REVIEW'S FIVE MUTANTS of the final (the adversarial review of 2026-09-30, finding 1), rewritten
here from its scratch scripts so they rebuild from this build's own tools; each must come out byte-identical to
the review's copy. x1/x4/x5 PASSED the old probe 7/7 (the finding); x2 and x3 it caught.
    python mutants_review.py <final link> <out dir>"""
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:80])
    return s.replace(old, new, 1)
M = {}
# x1 "freeze out" (brief stage 1) broken: the old freeze (radius 230, 9 damage, 3 entangle, 1.3s) kept in the row
# BESIDE the new root, and the rootfast branch falling through to fireUlt's generic tail.       -> [8]
s = one(src, '          rootFor:1.0,\n', '          rootFor:1.0, radius:230, dmg:9, apply:{entangle:3}, freeze:1.3,\n')
s = one(s, '      f.rootTally.casts++;\n      return;\n    }\n', '      f.rootTally.casts++;\n    }\n')
M["x1-freeze-kept"] = s
# x2 "for a second" broken: the root holds 0.8s (the design's 6.3 alternative) while the row says 1.0  -> [3]
M["x2-root-0.8"] = one(src, '    const hold = u.rootFor;\n', '    const hold = 0.8;\n')
# x3 "a killing blow roots nobody" broken: the dead opponent is rooted too                         -> [2]
M["x3-kill-roots"] = one(src, '    if (!q.alive) return;\n    const hold = u.rootFor;\n', '    const hold = u.rootFor;\n')
AP = 'q.apply("entangle", u.extraEnt, f === this.a ? "a" : "b"); T.ent += u.extraEnt; }'
# x4 the root's entangle written past apply(): its clock set to 9s by hand after the design's +1  -> [6]
M["x4-entangle-clock"] = one(src, AP, AP + "\n    if (q.status.entangle) q.status.entangle.t = 9;")
# x5 "the cast resolves nothing" broken: the cast also holds the foe 1.3s (the old freeze's length) -> [8]
M["x5-cast-pins"] = one(src, "      f.rootTally.casts++;\n      return;\n",
    "      f.rootTally.casts++;\n      if (foe.alive){ foe.pinV = [foe.vx, foe.vy]; foe.pin = Math.max(foe.pin, 1.3); foe.pinMax = Math.max(foe.pinMax, 1.3); }\n      return;\n")
for name, s in M.items():
    p = out / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(f"{name:<18} {hashlib.sha256(s.encode()).hexdigest()[:16]}  ({len(s) - len(src):+d} chars)")
