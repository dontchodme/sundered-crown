"""v112 §6a: STAGE 6's CONTROLS -- mutants of the stage-6 link (sc-heartwood-b11-fx, ceba5e801f4cf91b), each one
or two exact-once text edits, for the probe's [9] (the voices) and [10] (the picture's hook), and engine_ab's control.
    python mutants6.py <S>   -> <S>/mut/mut-s6-*.html, shas printed"""
import hashlib, pathlib, sys
S = pathlib.Path(sys.argv[1]); M = S / "mut"; M.mkdir(exist_ok=True)
src = (S / "links" / "sc-heartwood-b11-fx.html").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "ceba5e801f4cf91b"
V = '    SFX.play("ult", { w: "heartwood-root" });\n'
ENT = '    if (u.extraEnt > 0){ q.apply("entangle", u.extraEnt, f === this.a ? "a" : "b"); T.ent += u.extraEnt; }\n'
MUT = {
    # [9]: a voice at every close of the window, the deaths' included (the design has no close voice)
    "s6-close-voice": [("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRoot = null; continue; }\n",
                        '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRoot = null; SFX.play("ult", { w: "heartwood-root" }); continue; }\n')],
    # [9]: the root's voice MOVED above the killing blow's return: every root still voiced once, and a killing
    # blow, which roots nobody, voiced too
    "s6-kill-voice": [(V + ENT, ENT),
                      ("    T.blows++;\n    if (!q.alive) return;\n", "    T.blows++;\n" + V + "    if (!q.alive) return;\n")],
    # [10]: the picture's hook writes the simulation: the held ball nudged 1e-9 when the root is marked
    "s6-grove-sim": [("            foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldOut = 0;\n",
                      "            foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldOut = 0;\n            foe.vx += 1e-9;\n")],
    # [10]: the picture's hook draws the fight's RNG for its motes
    "s6-grove-rng": [("          const B = this.groveBlade(f), k = f.groveMoteN++;\n",
                      "          const B = this.groveBlade(f), k = f.groveMoteN++; this.rng();\n")],
}
for name, edits in MUT.items():
    t = src
    for a, b in edits:
        assert t.count(a) == 1, (name, t.count(a))
        t = t.replace(a, b, 1)
    p = M / f"mut-{name}.html"; p.write_text(t, encoding="utf-8", newline="\n")
    print(f"mut-{name}.html  {hashlib.sha256(t.encode()).hexdigest()[:16]}")
