"""v102 stage 6: mutants of the fx link that the probe's [10] and [11] must fail (each one thing).

Ironhail's pattern (ironhail/s6/mutants6.py). Each mutant changes one line of the stage-6 link.
"""
import pathlib, hashlib
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone")
fx = (S / "links/sc-lodestone-b205-fx.html").read_text(encoding="utf-8")
assert hashlib.sha256(fx.encode()).hexdigest()[:16] == "7a095b143d66fbdb"
CLOSE = '      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lodestone-close" });\n'
HEX = '        foe.apply("hex", u.hex, f === this.a ? "a" : "b");\n'
TOUCH = '        SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });\n'
GATE = '      const Z = (this.over || !f.alive) ? null : f.ultRunes;\n'
REC = '        f.lodeFx.push({ k: T.touches, walls, x: foe.x, y: foe.y, t: 0, t0: this.t, pts: [foe.x, foe.y, 0] });\n'
WALLS = '      if (f.lodeFade > 0){ this._lodeWalls(m, f, G, P); this._lodeMotes(m, f, G, P); }\n'
MUT = {
  # [10]: the close voice on every close, a death's as well as the clock's (v70 6.2's close is the clock's)
  "mV1-close-on-death": [(CLOSE, '      if (Z.t >= Z.dur || !f.alive || !foe.alive) SFX.play("ult", { w: "lodestone-close" });\n')],
  # [10]: the touch's snap played BEFORE its hex lands (pitched one count short, under the cap)
  "mV2-touch-before-hex": [(TOUCH, ""), (HEX, TOUCH + HEX)],
  # [11]: the picture's tick nudges the foe it records (a sim write from a presentation hook)
  "mP1-lode-writes": [(REC, REC + "        foe.x += 1e-9;\n")],
  # [11]: a drawn frame writes the fighter whose walls it draws (headless fights never draw: only the drawn subset sees it)
  "mP2-draw-writes": [(WALLS, WALLS + "      if (f.lodeFade > 0) f.vx += 1e-9;\n")],
  # [11]: the walls read `ultRunes` alone (the picture lab's ld-ungated control): lit through the verdict of a kill
  "mP3-ungated": [(GATE, "      const Z = f.ultRunes;\n")],
}
out = S / "s6/mut"; out.mkdir(exist_ok=True)
for name, reps in MUT.items():
    t = fx
    for a, b in reps:
        assert t.count(a) == 1, (name, a[:60])
        t = t.replace(a, b, 1)
    p = out / f"sc-lodestone-{name}.html"
    p.write_text(t, encoding="utf-8", newline="\n")
    print(f"{name:<24} {hashlib.sha256(t.encode()).hexdigest()[:16]}  {len(t) - len(fx):+d} chars")
