"""v110 §3's controls: scratch mutants of the final halo link, each breaking ONE sentence of v82
§1/§4 in a way that changes fights. Each must fail its own probe check and only that one.
    python mutants.py <final link> <out dir>"""
import pathlib, sys, hashlib
src, outd = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
base = src.read_text(encoding="utf-8")
def one(s, a, b):
    assert s.count(a) == 1, (s.count(a), a)
    return s.replace(a, b, 1)
M = {
  # [1] the window's clock: the halo also ticks through every freeze (the lab's clock)
  "m1-frozen": [("      if (L.t >= L.dur) this.blast(L);\n", "      this.tickHalo(dt);   // MUTANT\n      if (L.t >= L.dur) this.blast(L);\n"),
                ("      if (S.t >= S.dur) this.releaseSplit();\n", "      this.tickHalo(dt);   // MUTANT\n      if (S.t >= S.dur) this.releaseSplit();\n"),
                ("      this.hitStop -= dt;\n", "      this.hitStop -= dt;\n      this.tickHalo(dt);   // MUTANT\n")],
  # [2] the inside test: the halo reaches a quarter-ball further than haloR + R
  "m2-radius": [("      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;\n",
                 "      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + 1.25 * R)) continue;   // MUTANT\n")],
  # [3] the smite: every 0.4s instead of every tickCd (0.5s)
  "m3-cadence": [("        Z.cd = u.tickCd;\n", "        Z.cd = u.tickCd * 0.8;   // MUTANT\n")],
  # [4] the blessing: she is blessed whether or not a foe is inside
  "m4-blessout": [("      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;\n",
                   "      if (u.bless > 0 && Z.bcd <= 0){ Z.bcd = u.blessCd; f.apply(\"blessing\", u.bless, f === this.a ? \"a\" : \"b\"); T.bless += u.bless; Z.mut = 1; }   // MUTANT\n"
                   "      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;\n"),
                  ("      if (u.bless > 0 && Z.bcd <= 0){\n", "      if (u.bless > 0 && Z.bcd <= 0 && !Z.mut){   // MUTANT\n")],
  # [5] "no damage": each smite also hurts the foe for 1
  "m5-hurt": [("        foe.apply(\"smite\", u.smite, side);\n", "        foe.apply(\"smite\", u.smite, side);\n        this.hurt(foe, 1, f);   // MUTANT\n")],
  # [6] arm D, not taken: every blow she lands in the window smites +1 more
  "m6-arrows": [("      if (k === \"curse\") foe.pushCurse(dmgBase, n);\n      foe.apply(k, n);\n",
                 "      if (k === \"curse\") foe.pushCurse(dmgBase, n);\n      foe.apply(k, n);\n      if (k === \"smite\" && self.ultHalo) foe.apply(\"smite\", 1);   // MUTANT\n")],
  # [7] the beam's heal kept: the cast still heals 28
  "m7-beamheal": [("      f.ultHalo = { t: 0, dur: u.dur, cd: 0, bcd: 0 };\n",
                   "      f.ultHalo = { t: 0, dur: u.dur, cd: 0, bcd: 0 };\n      f.hp = Math.min(f.maxHp, f.hp + 28);   // MUTANT\n")],
}
outd.mkdir(parents=True, exist_ok=True)
for name, eds in M.items():
    s = base
    for a, b in eds: s = one(s, a, b)
    p = outd / f"sc-aureole-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(name, hashlib.sha256(s.encode()).hexdigest()[:16])
