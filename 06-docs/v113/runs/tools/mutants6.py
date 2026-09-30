"""Stage 6's mutants: copies of the fx link, each with ONE change the probe's [9] or [10] must catch.
mV1 a close voice: every window close -- by its clock OR BY A DEATH -- plays a crackle (fights identical)
mP1 the picture writes the simulation: the snare's picture lengthens the pin by 0.05 s (fights move)
mP2 the picture writes an invisible field: tickBrier stamps `lastBrier` on the fighter (fights identical)
Each is text on the link (the builder would refuse all three), written to <S>/mut6/."""
import hashlib, pathlib, sys
S = pathlib.Path(sys.argv[1])
src = (S / "links/sc-thornwake-b26.5-fx.html").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "d306822d6914c08c"
M = {
    "mV1-closevoice": ("        if (Z.t >= Z.dur || !f.alive || !foe.alive) f.ultBramble = null;\n",
                       '        if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultBramble = null; SFX.play("ult", { w: "thornwake-crackle" }); }\n'),
    "mP1-picwrite": ("        foe.brierHeld = 1; foe.brierRootFade = 1; foe.brierHeldOut = 0;\n",
                     "        foe.brierHeld = 1; foe.brierRootFade = 1; foe.brierHeldOut = 0; foe.pin += 0.05;\n"),
    "mP2-invisible": ("      if (f.brierTagT > 0) f.brierTagT -= dt;\n",
                      "      if (f.brierTagT > 0) f.brierTagT -= dt;\n      f.lastBrier = f.brierTagT;\n"),
}
out = S / "mut6"; out.mkdir(exist_ok=True)
lines = []
for name, (a, b) in M.items():
    assert src.count(a) == 1, name
    t = src.replace(a, b, 1)
    p = out / f"{name}.html"
    p.write_text(t, encoding="utf-8", newline="\n")
    lines.append(f"{name:<16} {hashlib.sha256(t.encode()).hexdigest()[:16]}  -{a.strip()}\n{'':<34}+{b.strip()}")
text = "\n".join(lines) + "\n"
(S / "runs" / "stage6_mutants_build.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
