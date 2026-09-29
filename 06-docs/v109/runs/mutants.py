"""SCRATCH MUTANTS of the final Consecration link (v109 §3). Each breaks ONE design sentence in a way that
changes fights; each must fail its own probe check and only that one.
    python mutants.py SRC OUTDIR"""
import sys, pathlib, hashlib
src, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
base = src.read_text(encoding="utf-8")
M = {
  # [1] "For a duration": the window 9s, not the builder's 8
  "m1-window": [('ult:{ name:"Consecration", charge:14, kind:"holyground", dur:8,',
                 'ult:{ name:"Consecration", charge:14, kind:"holyground", dur:9,')],
  # [2] "where it landed": the disc under the caster, not the struck ball
  "m2-plant": [("this.holyGround.push({ x: foe.x, y: foe.y, t0: this.holyT,",
                "this.holyGround.push({ x: self.x, y: self.y, t0: this.holyT,")],
  # [3] "a circle of holy ground that lasts" (8s): the discs go at 90% of their life
  "m3-life": [("if (this.holyT - d.t0 >= o.w.ult.groundLife) G.splice(i, 1);",
               "if (this.holyT - d.t0 >= o.w.ult.groundLife * 0.9) G.splice(i, 1);")],
  # [4] "is smitten": the smite's cooldown 20% short (every 0.4s)
  "m4-smite": [("          Z.cd = u.tickCd;\n", "          Z.cd = u.tickCd * 0.8;\n")],
  # [5] "Censer standing on holy ground is healed": the caster's ball, not its centre (the lab's test)
  "m5-heal": [("if (Math.hypot(f.x - d.x, f.y - d.y) < u.groundR) selfOn = true;",
               "if (Math.hypot(f.x - d.x, f.y - d.y) < u.groundR + R) selfOn = true;")],
  # [6] "No damage": a smite tick also hurts 2 (the lab's rejected tickDmg)
  "m6-dmg": [('          foe.apply("smite", u.smite, side);\n',
              '          foe.apply("smite", u.smite, side);\n          this.hurt(foe, 2, f);\n')],
  # [7] "the nova is out": the cast still lays the nova's 3 Smite
  "m7-nova": [("      f.holyTally.casts++;\n      return;\n",
               "      f.holyTally.casts++;\n      foe.apply(\"smite\", 3);\n      return;\n")],
  # [8] "the hammer swings as ever": the hammer 10% heavier in the window
  "m8-blade": [("    let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.w.dmg)",
                "    let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.w.dmg * (self.ultHoly ? 1.1 : 1))")],
  # [9] the charge: the lab's 16 unconverted
  "m9-charge": [('ult:{ name:"Consecration", charge:14, kind:"holyground",',
                 'ult:{ name:"Consecration", charge:16, kind:"holyground",')],
  # [1] the window clock: the ground's ticker also on hit-stop steps (the lab's clock)
  "m10-clock": [("      this.decayImpactOnly(dt);\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.",
                 "      this.decayImpactOnly(dt);\n      this.tickHolyGround(dt);   // MUTANT: the lab's clock\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.")],
}
outdir.mkdir(parents=True, exist_ok=True)
for name, reps in M.items():
    s = base
    for old, new in reps:
        n = s.count(old)
        assert n == 1, (name, n, old[:70])
        s = s.replace(old, new, 1)
    p = outdir / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(f"{name:10} {p.name:24} {hashlib.sha256(s.encode()).hexdigest()[:16]}")
