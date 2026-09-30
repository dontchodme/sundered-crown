"""The review's own two stage-2 controls, rebuilt on the FIXED stage-2 link: the builder's stage-2 code
plus ONE extra line in tickUnmake (on a window frame). The pre-review probe passed both 6/6.
    python review_stage2.py <stage-2 link> <out dir>"""
import pathlib, sys, hashlib
src, outd = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
base = src.read_text(encoding="utf-8")
TICK = "      f.unmakeTally.foeHex += foe.stacks(\"hex\");\n"
assert base.count(TICK) == 1
outd.mkdir(parents=True, exist_ok=True)
for name, line in (("q2-hexclock", "      foe.hexClock += 0.5;   // REVIEW CONTROL\n"),
                   ("q2-shrink", "      foe.reachMul = Math.max(0.4, foe.reachMul - 0.0005);   // REVIEW CONTROL\n")):
    s = base.replace(TICK, TICK + line, 1)
    p = outd / f"sc-spellbreaker-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(name, hashlib.sha256(s.encode()).hexdigest()[:16])
