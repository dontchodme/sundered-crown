"""Stage 6's probe controls: the fx link with ONE thing wrong each (scratch pages, never links).
  mV1  the fold played on EVERY close (a death's too)          -> must fail [9] alone
  mP1  tickBulwark nudges the foe 1e-9 on a bank               -> must fail [10] alone (and moves fights)
  mD1  a drawn frame nudges the caster 1e-9 (_bulwarkBar)      -> must fail [10] alone, on the drawn subset only
  mS1  a block writes a NEW underscore key into SHAPES (the sim) -> must fail [7] alone (the memo absorption is a draw's only)
  mS2  a block writes the renderer's own memo SHAPES._t (the sim)  -> must fail [7] alone
  (A first mS1 set `SHAPES._fxc.lk`: once a drawn Axiom fight has made `_fxc` the renderer's Map, that is an
  own property of a Map, which JSON -- entries only -- cannot see; it passed. The known JSON limit, v107 §3.)"""
import hashlib, pathlib
S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper")
fx = (S / "links/sc-lightkeeper-bulwark-b9.5-fx.html").read_text(encoding="utf-8")
M = {
 "mV1": ('      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });\n',
         '      if (Z.t >= Z.dur || !f.alive || !foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });\n'),
 "mP1": ('          this.float(f.x, f.y - 44, "+" + got, AFFINITIES.vigil.glow, 22 + got * 0.5);\n',
         '          foe.vx += 1e-9;\n          this.float(f.x, f.y - 44, "+" + got, AFFINITIES.vigil.glow, 22 + got * 0.5);\n'),
 "mS1": ('      SFX.play("ult", { w: "lightkeeper-gong" });\n',
         '      SFX.play("ult", { w: "lightkeeper-gong" });\n'
         '      SHAPES._lk = (SHAPES._lk || 0) + 1;\n'),
 "mS2": ('      SFX.play("ult", { w: "lightkeeper-gong" });\n',
         '      SFX.play("ult", { w: "lightkeeper-gong" });\n'
         '      SHAPES._t = 0;\n'),
 "mD1": ('    const th = f.theta, ux = Math.cos(th), uy = Math.sin(th);\n',
         '    f.x += 1e-9;\n    const th = f.theta, ux = Math.cos(th), uy = Math.sin(th);\n'),
}
for k, (a, b) in M.items():
    assert fx.count(a) == 1, k
    t = fx.replace(a, b, 1)
    p = S / f"s6int/mut/sc-lightkeeper-{k}.html"
    p.write_text(t, encoding="utf-8", newline="\n")
    print(k, hashlib.sha256(t.encode()).hexdigest()[:16], p.name)
