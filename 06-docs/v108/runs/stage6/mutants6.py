"""v108 stage 6: mutants of the fx link that the probe's [10] and [11] must fail (each one thing)."""
import pathlib, hashlib
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail")
fx = (S / "links/sc-ironhail-sunder-fx.html").read_text(encoding="utf-8")
LAND = '      SFX.play("ult", { w: "ironhail-land", n: foe.stacks("sunder") });\n'
SUND = '      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }\n'
CLOSE = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHail = null; continue; }\n'
TAG = '          if (hit && foe.alive && foe.hp > 0){\n'
RUNE = '  _quarrelRune(c, d, al, D){\n'
PUFF = '          f.quarrelFx.push({ x: d.x, y: d.y, r: u.hitR, t: 0, hit, n, s: side === "a" ? 0 : 1,'
MUT = {
  # [10]: the landing's thud pitched BEFORE its sunder (the count one short, off the cap)
  "mS1-land-before-sunder": [(LAND, ""), (SUND, LAND + SUND)],
  # [10]: a thud on every window close, on a death as on the clock (the design's close is silent)
  "mS2-close-voice": [(CLOSE, '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ SFX.play("ult", { w: "ironhail-miss" }); f.ultHail = null; continue; }\n')],
  # [11]: the picture's tick nudges the foe it tags (a sim write from a presentation hook)
  "mS3-quarrel-writes": [(TAG, TAG + "            foe.x += 1e-9;\n")],
  # [11]: a drawn frame writes the bolt it draws (headless fights never draw, so only the drawn subset sees it)
  "mS4-draw-writes": [(RUNE, RUNE + "    d.x += 1e-9;\n")],
  # [11]: a puff at the foe's spot instead of its bolt's
  "mS5-puff-at-foe": [(PUFF, '          f.quarrelFx.push({ x: foe.x, y: foe.y, r: u.hitR, t: 0, hit, n, s: side === "a" ? 0 : 1,')],
}
out = S / "s6/mut"; out.mkdir(exist_ok=True)
for name, reps in MUT.items():
    t = fx
    for a, b in reps:
        assert t.count(a) == 1, (name, a[:60])
        t = t.replace(a, b, 1)
    p = out / f"sc-ironhail-{name}.html"
    p.write_text(t, encoding="utf-8", newline="\n")
    print(f"{name:<24} {hashlib.sha256(t.encode()).hexdigest()[:16]}  {len(t) - len(fx):+d} chars")
