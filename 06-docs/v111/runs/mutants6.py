"""Stage 6's probe controls: scratch copies of the fx link, ONE edit each, each built to break one claim of
[7] or [8] (and, where the claim is presentation only, nothing else). Writes mutants6/<name>.html and prints
their sha256[:16]."""
import hashlib, pathlib
SB = pathlib.Path("<scratch>")
FX = SB / "links/sc-spellbreaker-b7.5-fx.html"
src = FX.read_text(encoding="utf-8")
M = [
 ("mV1-closedeath", "[7]", "the close voice on EVERY close of the window, a death's too",
  '      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "spellbreaker-close" });',
  '      if (Z.t >= Z.dur || !f.alive || !foe.alive) SFX.play("ult", { w: "spellbreaker-close" });'),
 ("mV2-stunx1", "[7]", "the stun voice on EVERY hex proc, x1 too",
  '        if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });',
  '        if (f.hexStunMul > 0) SFX.play("ult", { w: "spellbreaker-stun" });'),
 ("mP1-picwrite", "[8]", "tickUnmaking nudges the foe 1e-9 at a HEX +2 relabel (a sim write)",
  '          g.val = val; g.unmk = true; k--;',
  '          g.val = val; g.unmk = true; k--; (f === this.a ? this.b : this.a).vx += 1e-9;'),
 ("mG1-greyx1", "[8]", "the grey on EVERY hex proc, x1 too (a plain stun greyed)",
  '      if (hc < f.unmkHC && f.unmkMul > 1)',
  '      if (hc < f.unmkHC && f.unmkMul > 0)'),
 ("mD1-drawwrite", "[8]", "drawUnmaking nudges side a 1e-9 when it draws (drawn frames only)",
  '    for (const f of [a, b]) if (f.unmkMotes && f.unmkMotes.length) this._unmkMotes(c, m, f);',
  '    for (const f of [a, b]) if (f.unmkMotes && f.unmkMotes.length) this._unmkMotes(c, m, f);\n    m.a.vy += 1e-9;'),
]
print(f"fx link {FX.name} {hashlib.sha256(src.encode()).hexdigest()[:16]}")
for name, chk, how, old, new in M:
    assert src.count(old) == 1, name
    s = src.replace(old, new, 1)
    p = SB / "mutants6" / f"sc-spellbreaker-{name}.html"
    p.write_bytes(s.encode("utf-8"))
    print(f"{name:16s} {hashlib.sha256(s.encode()).hexdigest()[:16]}  breaks {chk}  {how}")
