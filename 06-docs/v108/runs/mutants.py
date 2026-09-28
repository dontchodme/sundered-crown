"""Probe controls for v108 §3: scratch mutants of the final link, each breaking ONE sentence of
v83 §1/§4 in a way that changes fights. Each must fail its own probe check and only that one."""
import pathlib, sys, hashlib
S = pathlib.Path(sys.argv[1]); src = (S / "links" / "sc-ironhail-b14.html").read_text(encoding="utf-8")
M = {
 "m2-cadence":  ("        Z.cd = u.dropCd;\n", "        Z.cd = u.dropCd * 0.9;\n"),                 # [2] a bolt every 0.36s
 "m3-fall":     ("      if (d.t < u.fallT){ i++; continue; }\n", "      if (d.t < u.fallT * 0.9){ i++; continue; }\n"),   # [3] lands 0.27s later
 "m4-sundermul":("      this.hurt(foe, u.dropDmg, f);\n", "      this.hurt(foe, u.dropDmg * foe.dmgTakenMul(), f);\n"),   # [4] the sunder multiplier on a landing
 "m5-missund":  ("_T.missed++; continue; }\n", "_T.missed++; if (foe.alive && u.sunder > 0) foe.apply(\"sunder\", u.sunder, d.side); continue; }\n"),  # [5] a miss sunders
 "m6-stop":     ("      T.dealt += before - (foe.hp + foe.shield);\n      if (u.sunder > 0){",
                 "      T.dealt += before - (foe.hp + foe.shield);\n      this.hitStop = Math.max(this.hitStop, 0.05);\n      if (u.sunder > 0){"),  # [6] a landing stops the world
 "m8-bowquiet": ("    if (!S || !f.alive || this.over) return;\n", "    if (!S || !f.alive || this.over || f.ultHail) return;\n"),  # [8] the bow stops firing in the window
}
for k, (a, b) in M.items():
    s = src
    if k == "m5-missund":
        a = "{ T.missed++; continue; }\n"; b = "{ T.missed++; if (foe.alive && u.sunder > 0) foe.apply(\"sunder\", u.sunder, d.side); continue; }\n"
    assert s.count(a) == 1, (k, a)
    s = s.replace(a, b, 1)
    out = S / "tmp" / f"mut-{k}.html"
    out.write_text(s, encoding="utf-8", newline="\n")
    print(k, hashlib.sha256(s.encode()).hexdigest()[:16])
