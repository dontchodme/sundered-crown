"""Stage 6's probe controls: scratch copies of the fx link, one change each (exactly-once text edits).
  mV1-closevoice  the close voice on EVERY close of the window (the clock's and a death's)      -> [9] alone
  mV2-enterfirst  the entry note on a window's FIRST tick too (a foe already inside at the cast) -> [9] alone
  mP1-picwrite    tickBenediction nudges the foe 1e-9 at a SMITE tag (a sim write)             -> [10] alone (fights move)
  mT1-tagevery    the SMITE tag on every smite, not each inside stretch's first (presentation)  -> [10] alone (fights identical)
  mD1-drawwrite   drawBenediction nudges side a 1e-9 when it draws (only a DRAWN frame)          -> [10] alone, drawn subset only
"""
import hashlib, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
FX = S / "links" / "sc-aureole-b12.5-fx.html"
t = FX.read_text(encoding="utf-8")
assert hashlib.sha256(t.encode()).hexdigest()[:16] == "f3228d8d1509edbb"
M = {
 "mV1-closevoice": ('      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });\n',
                    '      if (Z.t >= Z.dur || !f.alive || !foe.alive) SFX.play("ult", { w: "aureole-close" });\n'),
 "mV2-enterfirst": ('      if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });\n',
                    '      if (voiceIn && Z.voiceIn !== 1) SFX.play("ult", { w: "aureole-enter" });\n'),
 "mP1-picwrite": ("        f.beneTagS = true;\n", "        f.beneTagS = true; foe.vx += 1e-9;\n"),
 "mT1-tagevery": ("      if (dS > 0 && !f.beneTagS){\n", "      if (dS > 0){\n"),
 "mD1-drawwrite": ("    const c = this.ctx, n = m.inset || 0;\n", "    const c = this.ctx, n = m.inset || 0;\n    a.vy += 1e-9;\n"),
}
for name, (old, new) in M.items():
    assert t.count(old) == 1, (name, t.count(old))
    u = t.replace(old, new, 1)
    p = S / "s6" / "mut6" / f"sc-aureole-{name}.html"
    p.write_text(u, encoding="utf-8", newline="\n")
    print(f"{name:16s} {hashlib.sha256(u.encode()).hexdigest()[:16]}  {p.name}")
