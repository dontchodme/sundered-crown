#!/usr/bin/env python
"""SCRATCH MUTANTS of the final Angelus link (v104 §3). Each breaks ONE sentence
of the design in a way that changes fights; each must fail its own probe check
and only that one.  Usage: make_mutants.py <final link> <out dir>"""
import sys, hashlib, pathlib
src, outd = sys.argv[1], pathlib.Path(sys.argv[2])
s0 = pathlib.Path(src).read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:70])
    return s.replace(old, new, 1)
ADV = " for (const q of [this.a, this.b]) if (q.ultRise) q.ultRise.t += dt;   /* MUTANT m2-clock */"
M = {
  # [1] "hangs in the air at (W/2, 300)": it hangs 10 units higher
  "m1-hang": [("      f.x = tx; f.y = ty;\n      T.litFrames++;", "      f.x = tx; f.y = ty - 10;\n      T.litFrames++;")],
  # [9] "the window 8s" on the window tickers' clock: the rise's clock also runs
  # through every frozen step (hit stop, latch, split hold) -- the lab's clock
  "m2-clock": [("      this.hitStop -= dt;\n      this.t += dt;\n",
                "      this.hitStop -= dt;\n      this.t += dt;" + ADV + "\n"),
               ("      L.t += dt;\n      this.t += dt;\n",
                "      L.t += dt;\n      this.t += dt;" + ADV + "\n"),
               ("    if (this.splitHold){\n      const S = this.splitHold;\n      S.t += dt;\n      this.t += dt;\n",
                "    if (this.splitHold){\n      const S = this.splitHold;\n      S.t += dt;\n      this.t += dt;" + ADV + "\n")],
  # [3] "released to rest on close": the close keeps the banked velocity
  "m3-release": [("        if (f.alive){ f.vx = 0; f.vy = 0; }\n        continue;\n      }\n      T.frames++;\n      f.pin = Z.dur;",
                  "        continue;\n      }\n      T.frames++;\n      f.pin = Z.dur;")],
  # [4] "reachMul 10": half the reach (5, 344 units from the centre) stops short
  # of the floor from y 300. (A 0.95 cut, 9.5, still spans the hall and moved
  # the win rate by nothing: runs/probe_mut_m4-reach, kept as the record.)
  "m4-reach50": [("if (!Z.lit){ Z.lit = 1; f.reachMul = u.shaft; T.arrivals++; }", "if (!Z.lit){ Z.lit = 1; f.reachMul = u.shaft * 0.5; T.arrivals++; }")],
  # [5] "spin x 0.5": the shafts turn at the blades' full spin
  "m5-spin": [("* (f.ultRise && f.ultRise.lit ? f.w.ult.shaftSpin : 1) * f.spinMul(mods.spin)", "* (f.ultRise && f.ultRise.lit ? 1 : 1) * f.spinMul(mods.spin)")],
  # [6] "a shaft ... is a light hit": the shaft hits at full damage
  "m6-dmg": [("self.ultRise && self.ultRise.lit ? self.w.dmg * self.w.ult.winDmg : ", "")],
  # [7] "every hit heals": two blessing stacks a shaft hit
  "m7-heal": [('f.apply("blessing", u.healPer * n, f === this.a ? "a" : "b");', 'f.apply("blessing", 2 * u.healPer * n, f === this.a ? "a" : "b");')],
  # [2] "pinned there (pinFree 1, re-armed)": the per-frame re-arm drops pinFree
  # (review r2's r1). Nothing on the roster clears pinFree inside a window, so
  # on natural fights this mutant plays b9's fights exactly; the probe's forced
  # clears (every 50th window tick) are what make it fail -- and, under them,
  # change fights (the un-freed hold stuns the blades: tickStasis).
  "m8-pinfree": [("      T.frames++;\n      f.pin = Z.dur; f.pinMax = Z.dur; f.pinFree = 1;\n",
                  "      T.frames++;\n      f.pin = Z.dur; f.pinMax = Z.dur;\n")],
}
outd.mkdir(parents=True, exist_ok=True)
for k, eds in M.items():
    s = s0
    for o, n in eds: s = one(s, o, n)
    p = outd / f"sc-angelus-{k}.html"
    if p.exists(): raise SystemExit(f"refusing to overwrite {p}")
    p.write_text(s, encoding="utf-8", newline="\n")
    print(p.name, hashlib.sha256(s.encode()).hexdigest()[:16])
