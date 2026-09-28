"""Probe controls for v108 §3 (after the review): scratch mutants of THE FINAL LINK,
sc-ironhail-sunder, each breaking ONE sentence of v83 §1/§4 in a way that changes fights
(m7 excepted, and said: a fatal beat is presentation). Each must fail its own probe check and
only that one. Written to <S>/tmp/mut2-*.html; never a link."""
import pathlib, sys, hashlib
S = pathlib.Path(sys.argv[1]); src = (S / "links" / "sc-ironhail-sunder.html").read_text(encoding="utf-8")
M = {
 # [1] the window ticks through a hit stop (the lab's clock, the hit stop only)
 "m1-frozen":   ("      this.hitStop -= dt;\n", "      this.hitStop -= dt;\n      this.tickHail(dt);\n"),
 # [2] a bolt every 0.36s
 "m2-cadence":  ("        Z.cd = u.dropCd;\n", "        Z.cd = u.dropCd * 0.9;\n"),
 # [3] a bolt lands 0.27s after it drops
 "m3-fall":     ("      if (d.t < u.fallT){ i++; continue; }\n", "      if (d.t < u.fallT * 0.9){ i++; continue; }\n"),
 # [4] a landing multiplied by the foe's sunder (not flat)
 "m4-sundermul":("      this.hurt(foe, u.dropDmg, f);\n", "      this.hurt(foe, u.dropDmg * foe.dmgTakenMul(), f);\n"),
 # [5] a miss sunders too
 "m5-missund":  ("{ T.missed++; continue; }\n", "{ T.missed++; if (foe.alive && u.sunder > 0) foe.apply(\"sunder\", u.sunder, d.side); continue; }\n"),
 # [6] a landing stops the world for 0.05s
 "m6-stop":     ("      T.dealt += before - (foe.hp + foe.shield);\n      if (u.sunder > 0){",
                 "      T.dealt += before - (foe.hp + foe.shield);\n      this.hitStop = Math.max(this.hitStop, 0.05);\n      if (u.sunder > 0){"),
 # [7] a killing landing files no beat (DOES NOT CHANGE FIGHTS: the beat is presentation; kept as coverage)
 "m7-nobeat":   ("      if (wasUp && foe.hp <= 0)\n        this.beat({ kind: \"hit\", side: d.side === \"a\" ? 0 : 1,\n",
                 "      if (false && wasUp && foe.hp <= 0)\n        this.beat({ kind: \"hit\", side: d.side === \"a\" ? 0 : 1,\n"),
 # [8] the bow silent while the hail falls
 "m8-bowquiet": ("    if (!S || !f.alive || this.over) return;\n", "    if (!S || !f.alive || this.over || f.ultHail) return;\n"),
 # [8] partial (the review's r3-halfbow): the bow at half its cadence while the hail falls
 "m8b-halfbow": ("    f.fireCd += S.cadence * cm;\n", "    f.fireCd += S.cadence * cm * (f.ultHail ? 2 : 1);\n"),
 # [9] the nova is not gone (the review's r1-novakept): the hail's cast also fires fourteen arrows
 "m9-novakept": ("      f.hailTally.casts++;\n      return;\n",
                 "      f.hailTally.casts++;\n      if (f.w.shot) for (let i = 0; i < 14; i++) this.spawnShot(f, f.theta + (i / 14) * TAU);\n      return;\n"),
}
for k, (a, b) in M.items():
    assert src.count(a) == 1, (k, src.count(a))
    s = src.replace(a, b, 1)
    out = S / "tmp" / f"mut2-{k}.html"
    out.write_text(s, encoding="utf-8", newline="\n")
    print(k, hashlib.sha256(s.encode()).hexdigest()[:16])
