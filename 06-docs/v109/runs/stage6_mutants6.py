"""Stage 6's probe controls: scratch copies of the fx link, one change each (exactly-once text edits).
  mV1-closevoice  a heal chime on EVERY close of the window (the clock's and a death's)      -> [10] alone
  mP1-picwrite    tickConsecration nudges the foe 1e-9 on a smite tick (a sim write)         -> [11] alone (fights move)
  mT1-tagevery    the SMITE tag on every smite tick, not each stretch's first (presentation) -> [11] alone (fights identical)
  mD1-drawwrite   drawConsecration nudges side a 1e-9 when it draws (only a DRAWN frame)     -> [11] alone, drawn subset only
"""
import hashlib, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
FX = S / "links" / "sc-censer-consecration-b25.5-fx.html"
t = FX.read_text(encoding="utf-8")
assert hashlib.sha256(t.encode()).hexdigest()[:16] == "3d68c7648a9cb3a8"
M = {
 "mV1-closevoice": ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHoly = null; continue; }\n      const u = f.w.ult, T = f.holyTally, R = CONFIG.physics.ballR;",
                    "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHoly = null; SFX.play(\"spark\", { collect: true, n: 1 }); continue; }\n      const u = f.w.ult, T = f.holyTally, R = CONFIG.physics.ballR;"),
 "mP1-picwrite": ("      if (dK > 0) f.consPulse = 1;\n", "      if (dK > 0){ f.consPulse = 1; foe.vx += 1e-9; }\n"),
 "mT1-tagevery": ("      if (dK > 0 && !f.consTagS){\n", "      if (dK > 0){\n"),
 "mD1-drawwrite": ("    const c = this.ctx, n = m.inset || 0;\n", "    const c = this.ctx, n = m.inset || 0;\n    a.vy += 1e-9;\n"),
}
for name, (old, new) in M.items():
    assert t.count(old) == 1, (name, t.count(old))
    u = t.replace(old, new, 1)
    p = S / "s6" / "mut6" / f"sc-censer-{name}.html"
    p.write_text(u, encoding="utf-8", newline="\n")
    print(f"{name:16s} {hashlib.sha256(u.encode()).hexdigest()[:16]}  {p.name}")
