# Scratch control builds of a Lodestone link (never a chain link). One edit each, exactly once, or refuse.
import pathlib, sys, hashlib
src, out, which = sys.argv[1], sys.argv[2], sys.argv[3]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, (which, old[:80], s.count(old)); return s.replace(old, new, 1)
OVER = "    if (this.over){ this.decay(dt); return; }\n"
if which == "labclock":      # the runes' window clock and cooldown run through freezes; touches in freezes
    s = one(s, OVER, OVER + "    if (this.hitStop > 0 || this.latch || this.splitHold) this.tickRunes(dt);   // CONTROL: the lab's clock\n")
elif which == "after":       # the ticker after tickHits/checkEnd on the normal path only (the lab's order, the engine's clock)
    s = one(s, "    this.tickRunes(dt);                 // REBUTTAL (v70)\n", "")
    s = one(s, "    this.checkEnd();\n    this.decay(dt);\n  }\n", "    this.checkEnd();\n    this.decay(dt);\n    this.tickRunes(dt);   // CONTROL: the lab's slot, after the whole step\n  }\n")
else:
    # MUTANTS (probe controls): each breaks one sentence of the design.
    T = {
     "mut-pad":   ("const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset, e = u.pad;",
                   "const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset, e = u.pad + 4.5;"),
     "mut-cd":    ("      Z.cd = u.cd;\n      T.touches++;", "      Z.cd = u.cd * 0.8;\n      T.touches++;"),
     "mut-hex2":  ('        foe.apply("hex", u.hex, f === this.a ? "a" : "b");', '        foe.apply("hex", u.hex + 1, f === this.a ? "a" : "b");'),
     "mut-impulse": ("        foe.vx = dx / d * u.hurl;\n        foe.vy = dy / d * u.hurl;",
                     "        foe.vx += dx / d * u.hurl;\n        foe.vy += dy / d * u.hurl;"),
     "mut-bite":  ("        T.hurls++;\n", "        T.hurls++;\n        this.hurt(foe, 4, f);\n"),
     "mut-dur":   ("      Z.t += dt;\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }",
                   "      Z.t += dt * 0.9;\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }"),
     # EQUIVALENT by design (review round 2): drops the foe-death close, which this engine cannot reach
     "mut-death": ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }",
                   "      if (Z.t >= Z.dur || !f.alive){ f.ultRunes = null; continue; }"),
     "mut-self":  ("      if (foe.pin > 0 || Z.cd > 0) continue;",
                   "      if (f.x <= this.inset + CONFIG.physics.ballR + u.pad) f.vx += 200;\n      if (foe.pin > 0 || Z.cd > 0) continue;"),
     # REVIEW ROUND 3: invented effects outside the probe's old field lists (the review's rv-drain, rv-spin, rv-dir,
     # re-made here from its mk_mut.py text), and two more of the same kind on the Match and on the caster.
     "rv-drain":  ("      Z.cd = u.cd;\n      T.touches++;", "      Z.cd = u.cd;\n      T.touches++;\n      foe.charge = Math.max(0, foe.charge - 1);"),
     "rv-spin":   ("      Z.cd = u.cd;\n      T.touches++;", "      Z.cd = u.cd;\n      T.touches++;\n      foe.spinDir = -foe.spinDir;"),
     "rv-dir":    ("        const dx = f.x - foe.x, dy = f.y - foe.y, d = Math.hypot(dx, dy) || 1;",
                   "        const dx = foe.x - f.x, dy = foe.y - f.y, d = Math.hypot(dx, dy) || 1;"),
     "mut-clank": ("      Z.cd = u.cd;\n      T.touches++;", "      Z.cd = u.cd;\n      T.touches++;\n      this.clankCd = Math.max(this.clankCd, 0.3);"),
     "mut-charge": ("      Z.cd = u.cd;\n      T.touches++;", "      Z.cd = u.cd;\n      T.touches++;\n      f.charge += 0.25;"),
    }
    old, new = T[which]; s = one(s, old, new)
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(which, pathlib.Path(out).name, hashlib.sha256(s.encode()).hexdigest()[:16])
