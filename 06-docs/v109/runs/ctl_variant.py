"""SCRATCH CONTROLS for v109 (never links of the chain). Each takes a built Consecration link and changes ONE thing.
    python ctl_variant.py SRC OUT KIND
KIND:
  labclock   the ground's clock runs through freezes, as the lab's did: tickHolyGround is also called on
             every frozen step (hit stop, latch, split hold), so the window, the cooldowns, the discs'
             lives and the tests run on step-seconds (v107's labclock, the same three insertions).
  ballheal   the caster is on the ground when its BALL touches a disc (groundR + R), the lab's test,
             instead of its centre within groundR (the build's reading 4, from v78 §4's prose).
  wholelife  the prose's other reading of "for as long as it stands there": the ground smites and heals
             for its whole 8s life, window or not, on cooldowns that persist from the first cast
             (the build's reading 2 is the lab's: only while the caster's window is open).
"""
import sys, pathlib, re, hashlib
src, out, kind = sys.argv[1], sys.argv[2], sys.argv[3]
s = pathlib.Path(src).read_text(encoding="utf-8")
def one(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new, 1)
if kind == "labclock":
    one("      this.decayImpactOnly(dt);\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.",
        "      this.decayImpactOnly(dt);\n      this.tickHolyGround(dt);   // CONTROL: the lab's clock\n      /* GRAVITY STILL ACTS, EVEN THOUGH NOTHING MOVES.")
    one("      if (L.t >= L.dur) this.blast(L);\n      return;",
        "      if (L.t >= L.dur) this.blast(L);\n      this.tickHolyGround(dt);   // CONTROL: the lab's clock\n      return;")
    one("      if (S.t >= S.dur) this.releaseSplit();\n      return;",
        "      if (S.t >= S.dur) this.releaseSplit();\n      this.tickHolyGround(dt);   // CONTROL: the lab's clock\n      return;")
elif kind == "ballheal":
    one("        if (Math.hypot(f.x - d.x, f.y - d.y) < u.groundR) selfOn = true;",
        "        if (Math.hypot(f.x - d.x, f.y - d.y) < u.groundR + R) selfOn = true;   // CONTROL: the lab's ball test")
elif kind == "wholelife":
    one("""    for (const f of [this.a, this.b]){
      const Z = f.ultHoly;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHoly = null; continue; }
      const u = f.w.ult, T = f.holyTally, R = CONFIG.physics.ballR;
      const side = f === this.a ? "a" : "b";
      T.frames++;
      T.foeStk += foe.stacks("smite");
      Z.cd -= dt;
      Z.bcd -= dt;
""", """    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a;
      /* CONTROL: the ground acts for its whole life, window or not */
      if (f.ultHoly){ f.ultHoly.t += dt; if (f.ultHoly.t >= f.ultHoly.dur || !f.alive || !foe.alive) f.ultHoly = null; }
      if (!f.holyTally || !f.alive || !foe.alive) continue;
      const Z = f.holyCdv || (f.holyCdv = { cd: 0, bcd: 0 });
      const u = f.w.ult, T = f.holyTally, R = CONFIG.physics.ballR;
      const side = f === this.a ? "a" : "b";
      T.frames++;
      T.foeStk += foe.stacks("smite");
      Z.cd -= dt;
      Z.bcd -= dt;
""")
else:
    raise SystemExit("unknown kind")
pathlib.Path(out).write_text(s, encoding="utf-8", newline="\n")
print(kind, pathlib.Path(out).name, hashlib.sha256(s.encode()).hexdigest()[:16])
