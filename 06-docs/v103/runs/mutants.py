"""PROBE CONTROLS (v103 §3): scratch mutants of the final Temper link, each breaking ONE
design sentence in a way that changes fights. Each must fail its own probe check and only
that one. Not links. usage: mutants.py <final link> <out dir>"""
import sys, pathlib, hashlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s0 = src.read_text(encoding="utf-8")
M = {
 # [2] as heavy as a warhammer: the clank weighs the twinblade's own 1.1
 "m2-clank-light": ("    const mA = A.w.mass * A.massMul, mB = B.w.mass * B.massMul;",
                    "    const mA = A.w.mass, mB = B.w.mass;"),
 # [2] as heavy as a warhammer, EVERY bind: the clank weighs the iron only when Coldiron is side A
 # (the whole-light m2 above leaves no won bind at all, so [3] goes unexercised: not a clean control)
 "m2b-clank-sideA": ("    const mA = A.w.mass * A.massMul, mB = B.w.mass * B.massMul;",
                     "    const mA = A.w.mass * A.massMul, mB = B.w.mass;"),
 # [3] each win sunders: one stack a won bind, not `bind`
 "m3-bind-one":    ('        temperL.apply("sunder", u.bind, temperW === this.a ? "a" : "b");',
                    '        temperL.apply("sunder", u.bind - 1, temperW === this.a ? "a" : "b");'),
 # [4] while the iron holds: the ceiling never comes back down after the first cast
 "m4-cap-stays":   ("      f.sunderCap = foe.ultTemper ? foe.w.ult.cap : STATUS.sunder.maxStacks;",
                    "      f.sunderCap = foe.ultTemper || foe.temperTally ? foe.w.ult.cap : STATUS.sunder.maxStacks;"),
 # [1] for a duration: the window 1% long on its clock
 "m1-window-long": ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        f.ultTemper = null;",
                    "      if (Z.t >= Z.dur * 1.01 || !f.alive || !foe.alive){\n        f.ultTemper = null;"),
 # [6] the declared gravity consequence: move falls at the twinblade's own weight
 "m6-move-light":  ("    f.vy += P.gravity * Math.pow((f.w.mass * f.massMul + f.burden * f.burdenMass)",
                    "    f.vy += P.gravity * Math.pow((f.w.mass + f.burden * f.burdenMass)"),
 # [7] nothing else: the window's first tick stops the world
 "m7-open-stop":   ("      Z.t += dt;\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        f.ultTemper = null;",
                    "      Z.t += dt;\n      if (Z.t === dt) this.hitStop = Math.max(this.hitStop, 0.05);\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        f.ultTemper = null;"),
 # [7] nothing else, v2: the window's CLOSE stops the world 0.1s. (m7 above is a no-op: its 0.05 stop
 # lands on the cast's frame, under the cast's own 0.08, so it changes no fight -- not a control.)
 "m7b-close-stop": ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        f.ultTemper = null;",
                    "      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        this.hitStop = Math.max(this.hitStop, 0.1);\n        f.ultTemper = null;"),
 # THE REVIEW'S TWO (the adversarial review of v103, 2026-09-27; scratchpad/review_coldiron/my_mutants.py, verbatim):
 # [1] the window tickers' clock: the window ALSO ticks on the hit-stop path, i.e. it runs on MATCH time
 # the way the lab's did. Still 960 ticks a window -- the first probe's tick count passed it 7/7.
 "r1-window-through-hitstop": ("    if (this.hitStop > 0){\n      this.hitStop -= dt;\n      this.t += dt;\n",
                               "    if (this.hitStop > 0){\n      this.hitStop -= dt;\n      this.t += dt;\n      this.tickTemper(dt);\n"),
 # [3] each bind it wins sunders THE LOSER: the opponent (this.a / this.b) instead (the lab's reading 2)
 "r2-sunder-opponent": ('        temperL.apply("sunder", u.bind, temperW === this.a ? "a" : "b");',
                        '        (temperW === this.a ? this.b : this.a).apply("sunder", u.bind, temperW === this.a ? "a" : "b");'),
}
for name, (a, b) in M.items():
    assert s0.count(a) == 1, (name, s0.count(a))
    s = s0.replace(a, b)
    p = out / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(p.name, hashlib.sha256(s.encode()).hexdigest()[:16])
