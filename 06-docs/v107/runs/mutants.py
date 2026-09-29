"""SCRATCH MUTANTS of the final Bulwark link (v107 probe controls). Each breaks ONE sentence in the
ticker's code (never the ult block's numbers, which the probe follows) in a way that changes fights.
    python mutants.py FINAL.html OUTDIR"""
import sys, pathlib, hashlib
src, outd = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
S0 = src.read_text(encoding="utf-8")
M = {
 # [1] "for a duration": the window 10% long on the window clock
 "m1-window": [("if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }",
                "if (Z.t >= Z.dur * 1.1 || !f.alive || !foe.alive){ f.ultWall = null; continue; }")],
 # [3] "arrows die on it": the kill zone 4 units wide of r + shotPad
 "m3-arrows": [("if (!(segDist(ax, ay, bx, by, s.x, s.y).d < (s.r || 6) + u.shotPad)) continue;",
                "if (!(segDist(ax, ay, bx, by, s.x, s.y).d < (s.r || 6) + u.shotPad + 4)) continue;")],
 # [4] "runs into it": the cooldown 10% short after a block
 "m4-cd": [("      Z.cd = u.cd;\n      T.blocks++;", "      Z.cd = u.cd * 0.9;\n      T.blocks++;")],
 # [5] "bounces off": the shove 10% strong
 "m5-shove": [("      foe.vx += kx / kl * u.shove;\n      foe.vy += ky / kl * u.shove;",
               "      foe.vx += kx / kl * u.shove * 1.1;\n      foe.vy += ky / kl * u.shove * 1.1;")],
 # [6] "the shield grows": a ball block banks one ward too many
 "m6-bank": [("        f.shield = Math.min(W.cap, f.shield + u.bankBall);",
              "        f.shield = Math.min(W.cap, f.shield + u.bankBall + 1);")],
 # [5] "along the wall's normal away from the caster's side", read LITERALLY: always outward (+facing),
 #     so a foe behind the wall is shoved away from the caster instead of back to its own side (review r3-side;
 #     also the size of the literal reading for v107 §6)
 "m8-side": [("      const side = ((foe.x - cx) * ux + (foe.y - cy) * uy) >= 0 ? 1 : -1;",
              "      const side = 1;")],
 # [7] "no hit stop": a block stops the world for 0.05s
 "m7-stop": [("      Z.cd = u.cd;\n      T.blocks++;", "      Z.cd = u.cd;\n      T.blocks++;\n      this.hitStop = Math.max(this.hitStop, 0.05);")],
 # SECOND REVIEW ROUND. [7] nothing else: a block also stuns the foe for 0.3s (the reviewer's r5-stun,
 #     character for character; it passed the first [7] 8/8 while Lightkeeper went 43.9% -> 76.1%)
 "r5-stun": [("      T.blocks++;\n", "      T.blocks++;\n      foe.stun = Math.max(foe.stun, 0.3);\n")],
 # [7] the status variant: a block also lays a stack of Hex on the foe (src a side letter, ruling 4)
 "r6-hex": [("      T.blocks++;\n", "      T.blocks++;\n      foe.apply(\"hex\", 1, f === this.a ? \"a\" : \"b\");\n")],
 # [2] "the nova is out" and the cast does nothing else: the cast also lays two Sunder on the foe
 "r7-castsunder": [("      f.wallTally.casts++;\n      return;",
                    "      f.wallTally.casts++;\n      foe.apply(\"sunder\", 2, f === this.a ? \"a\" : \"b\");\n      return;")],
 # THE REVIEWER'S OTHER FOUR (rev_lk/mine.py, the same replacements), re-run so the stricter probe is seen to keep
 # each of them to its own check:
 # [3] "a killed arrow is stuck, not spliced": a net arrow spliced like any other
 "r1-netsplice": [("        if (s.net){ s.stuck = true; s.vx = 0; s.vy = 0; s.life = 1e9; }\n        else this.shots.splice(i, 1);",
                   "        this.shots.splice(i, 1);")],
 # [4] "a foe ... not pinned": a pinned foe is blocked too
 "r2-pinned": [("      if (Z.cd > 0 || foe.pin > 0) continue;", "      if (Z.cd > 0) continue;")],
 # [2] the cast opens the cooldown already running
 "r3-castcd": [("      f.ultWall = { t: 0, dur: u.dur, cd: 0 };", "      f.ultWall = { t: 0, dur: u.dur, cd: u.cd };")],
 # [6] the arrow's bank without the ward clock
 "r4-noward": [("          f.shieldMax = Math.max(f.shieldMax, f.shield);\n          f.apply(\"ward\", 1);                       // (re)starts the clock\n          T.banks++;\n          T.banked += f.shield - b0;\n        }\n      }",
                "          f.shieldMax = Math.max(f.shieldMax, f.shield);\n          T.banks++;\n          T.banked += f.shield - b0;\n        }\n      }")],
 # THIRD REVIEW ROUND (the reviewer's review_lk/my_mutants.py, the same replacements). Both passed the v4 probe 8/8
 # while changing fights; under v5 each must fail [7] alone.
 # [7] / reading 8 "the target is the OPPONENT, never a Twinshade shade": a block also shoves any shade inside R + ballPad
 "v3-shade": [("      Z.cd -= dt;\n      if (Z.cd > 0 || foe.pin > 0) continue;",
               "      for (const sh of this.shades){ if (!sh.alive || !(segDist(ax, ay, bx, by, sh.x, sh.y).d < R + u.ballPad)) continue;\n"
               "        const sd = ((sh.x - cx) * ux + (sh.y - cy) * uy) >= 0 ? 1 : -1; sh.vx += ux * sd * 60; sh.vy += uy * sd * 60; }\n"
               "      Z.cd -= dt;\n      if (Z.cd > 0 || foe.pin > 0) continue;")],
 # [7] "nothing else": a block also writes the GLOBAL ward row (the pool ceiling), shared by every fighter and every
 #     later match on the page
 "v4-global": [("      Z.cd = u.cd;\n      T.blocks++;", "      Z.cd = u.cd;\n      T.blocks++;\n      STATUS.ward.cap = 120;")],
}
outd.mkdir(parents=True, exist_ok=True)
for name, reps in M.items():
    s = S0
    for old, new in reps:
        assert s.count(old) == 1, (name, s.count(old), old[:60])
        s = s.replace(old, new, 1)
    p = outd / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(f"{p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}")
