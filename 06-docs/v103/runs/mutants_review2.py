"""Reviewer-2 mutants of the final Coldiron link: each breaks one sentence the author did not mutate."""
import sys, pathlib, hashlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s0 = src.read_text(encoding="utf-8")
M = {
 # [1] the window closes on EITHER death (reading 4): drop the death close; a kill flight keeps the iron
 "q1-no-death-close": ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){\n        f.ultTemper = null;",
                       "      if (Z.t >= Z.dur){\n        f.ultTemper = null;"),
 # [4] the cap is THE FOE'S (reading 1): lift the caster's own ceiling instead of the foe's
 "q2-cap-own":        ("      f.sunderCap = foe.ultTemper ? foe.w.ult.cap : STATUS.sunder.maxStacks;",
                       "      f.sunderCap = f.ultTemper ? f.w.ult.cap : STATUS.sunder.maxStacks;"),
 # [5] the blades are still the blades: the iron blade hits 10% harder (an invented mechanic)
 "q3-iron-hits-harder": ("            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul();",
                         "            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul() * (self.massMul > 1 ? 1.1 : 1);"),
 # [3] a DECISIVE won bind only: a deadlock (the hammers) sunders too
 "q4-deadlock-sunders": ("    if (decisive && temperW.ultTemper){",
                         "    if (temperW.ultTemper){"),
}
for name, (a, b) in M.items():
    assert s0.count(a) == 1, (name, s0.count(a))
    s = s0.replace(a, b)
    p = out / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(p.name, hashlib.sha256(s.encode()).hexdigest()[:16])
