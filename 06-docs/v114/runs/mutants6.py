"""v114 scratch: stage 6's mutants -- the fx link with ONE thing of the picture or the voice broken, each
aimed at [11] or [12]. Written to <scratch>/mutants6/; nothing in the repo."""
import hashlib, pathlib
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard")
FX = W / "links" / "sc-goreshard-b10.25-fx.html"
g = FX.read_bytes().decode("utf-8")
M = [
    ("mV1-closevoice", "[11]", "the cast voice again at every window close, a death's included (a close voice)",
     "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultPrice = null; continue; }\n",
     "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ SFX.play(\"ult\", { w: f.w.id }); f.ultPrice = null; continue; }\n"),
    ("mV2-x1priced", "[11]", "the priced voice on every window blow, x1 ones included (price 0)",
     "    if (priceN > 0) SFX.play(\"hit\", { dmg, crit, price: priceN });\n",
     "    if (self.ultPrice) SFX.play(\"hit\", { dmg, crit, price: priceN });\n"),
    ("mP1-picwrite", "[12]", "tickGore nudges the foe's velocity 1e-9 at every mote it sheds (a sim write)",
     "          this._goreShed(f);\n",
     "          this._goreShed(f); foe.vx += 1e-9;\n"),
    ("mP2-glowfloor", "[12]", "the glow's floor 0.25, not v81's 0.2",
     "(0.2 + 0.15 * n - f.goreGlow)", "(0.25 + 0.15 * n - f.goreGlow)"),
    ("mP3-floatx2", "[12]", "the priced float x(1 + 0.2 n), not x(1 + 0.1 n)",
     "* (crit ? 1.3 : 1) * (1 + 0.1 * priceN);", "* (crit ? 1.3 : 1) * (1 + 0.2 * priceN);"),
    ("mP4-windowonly", "[12]", "the red read off the window alone (not the match, not both standing): held through the verdict when the kill leaves the window set",
     "      const open = !!f.ultPrice && !this.over && f.alive && foe.alive;\n",
     "      const open = !!f.ultPrice;\n"),
    ("mD1-drawwrite", "[12] drawn", "the blade's draw writes the caster's velocity (only a drawn frame can see it)",
     "    const run = !(f.goreOut > 0);\n",
     "    const run = !(f.goreOut > 0); f.vx += 1e-9;\n"),
]
for name, chk, what, a, b in M:
    assert g.count(a) == 1, (name, g.count(a))
    t = g.replace(a, b, 1)
    out = W / "mutants6" / f"sc-goreshard-{name}.html"
    out.write_bytes(t.encode("utf-8"))
    print(f"{name:<16} {chk:<11} {hashlib.sha256(t.encode()).hexdigest()[:16]}  {what}")
