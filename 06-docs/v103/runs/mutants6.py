"""Stage 6's controls: four one-line mutants of sc-coldiron-temper-fx, each built to fail ONE of the
probe's stage-6 checks ([8] the voice, [9] the picture) and nothing else it can see."""
import pathlib, hashlib
S = pathlib.Path(__file__).resolve().parent.parent
src = (S / "links/sc-coldiron-temper-fx.html").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "3693eda608b26fa8"
M = {
 # [8]: the close voiced on EVERY close, death closes included
 "mS1-close-on-death": ('        if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "coldiron-close" });',
                        '        SFX.play("ult", { w: "coldiron-close" });'),
 # [8]: the anvil carrying the count BEFORE the bind's sunder
 "mS2-anvil-count-before": ('        SFX.play("ult", { w: "coldiron-anvil", n: temperL.stacks("sunder") });',
                            '        SFX.play("ult", { w: "coldiron-anvil", n: temperL.stacks("sunder") - u.bind });'),
 # [9]: the picture's hook writes the sim (the foe nudged 1e-9 on a won bind)
 "mS3-iron-writes": ('        f.ironSeen = T.won;\n', '        f.ironSeen = T.won; foe.vx += 1e-9;\n'),
 # [9] on the DRAWN subset only: a draw writes the sim
 "mS4-draw-writes": ('''        && !a.ironSparks.length && !b.ironSparks.length) return;   // <- zero burden
''', '''        && !a.ironSparks.length && !b.ironSparks.length) return;   // <- zero burden
    a.vx += 1e-9;
'''),
}
for name, (old, new) in M.items():
    assert src.count(old) == 1, name
    t = src.replace(old, new, 1)
    (S / "s6/mut" / f"mut-{name}.html").write_text(t, encoding="utf-8", newline="\n")
    print(f"mut-{name}.html  {hashlib.sha256(t.encode()).hexdigest()[:16]}")
