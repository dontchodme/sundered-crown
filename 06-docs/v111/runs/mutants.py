"""v111 §3's controls: scratch mutants of the final Unmaking link, each breaking ONE sentence of v79
§1/§4 in a way that changes fights. Each must fail its own probe check and only that one.
m1-m6 are the build's own; r1-r5 were added after v111's adversarial review (r1-r3 are the reviewer's
own three, r4 and r5 cover the two bracket and cadence checks that review asked for).
    python mutants.py <final link> <out dir>"""
import pathlib, sys, hashlib
src, outd = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
base = src.read_text(encoding="utf-8")
def one(s, a, b):
    assert s.count(a) == 1, (s.count(a), a)
    return s.replace(a, b, 1)
TICK = "      f.unmakeTally.foeHex += foe.stacks(\"hex\");\n"
INS_END = "        self.unmakeTally.extra += U.hexExtra;\n      }\n    }\n"
M = {
  # [1] "for a duration" on the window clock: the window also runs through every freeze (the lab's clock)
  "m1-frozen": [("      if (L.t >= L.dur) this.blast(L);\n", "      this.tickUnmake(dt);   // MUTANT\n      if (L.t >= L.dur) this.blast(L);\n"),
                ("      if (S.t >= S.dur) this.releaseSplit();\n", "      this.tickUnmake(dt);   // MUTANT\n      if (S.t >= S.dur) this.releaseSplit();\n"),
                ("      this.hitStop -= dt;\n", "      this.hitStop -= dt;\n      this.tickUnmake(dt);   // MUTANT\n")],
  # [2] "every stun a hex lands lasts twice as long": the weapon's stun ignores the field (breakSpin still reads it)
  "m2-stunlen": [("        f.stun = Math.max(f.stun, STATUS.hex.stunFor * f.hexStunMul);\n",
                  "        f.stun = Math.max(f.stun, STATUS.hex.stunFor);   // MUTANT\n")],
  # [3] "the FOE's f.hexStunMul ... a runic foe's hexes on Spellbreaker are untouched": the lab's global --
  #     the caster's own hex stuns doubled too while its window is open
  "m3-global": [("      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : 1;\n",
                 "      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : f.ultUnmake ? f.w.ult.stunMul : 1;   // MUTANT\n")],
  # [4] "every hit hexes twice" -- in the window: the second hex on every blow, outside the window too
  "m4-hexout": [(INS_END, INS_END + "    else if (self.w.id === \"spellbreaker\") foe.apply(\"hex\", 1, self === this.a ? \"a\" : \"b\");   // MUTANT\n")],
  # [5] "nothing else": the window drags the foe (0.5% of its velocity a frame)
  "m5-drag": [(TICK, TICK + "      foe.vx *= 0.995; foe.vy *= 0.995;   // MUTANT\n")],
  # [6] "the bolt is out": the cast still hits for the bolt's 20
  "m6-boltkept": [("      f.ultUnmake = { t: 0, dur: u.dur };\n",
                   "      f.ultUnmake = { t: 0, dur: u.dur };\n      this.hurt(foe, 20, f);   // MUTANT\n")],
  # [4] (the review's r1) "every hit Spellbreaker lands hexes twice": the block's hexExtra 1 -> 0, so every hit hexes ONCE
  "r1-hexonce": [("          hexExtra:1,          // v79: the second hex (stage 3)\n",
                  "          hexExtra:0,          // MUTANT\n")],
  # [5] "nothing else": the window runs the foe's hex clock -- +0.01 a window frame, about half as fast again as
  #     2.5 stacks' own dt x stacks, so hexes proc more often while clean stun runs are left to measure. (The
  #     review's +0.5 a frame, a proc on almost every frame, is q2-hexclock on the stage-2 link; its first run on
  #     this link is runs/probe_mut_r2-hexclock-0.5.txt: [5], and [2] by the 200-run floor, since it leaves 3
  #     clean stun runs in windows to measure.)
  "r2-hexclock": [(TICK, TICK + "      foe.hexClock += 0.01;   // MUTANT\n")],
  # [5] (the review's) "nothing else" / §3 arm D, no shrink: the rejected shrink carried into the ticker, never restored
  "r3-shrink": [(TICK, TICK + "      foe.reachMul = Math.max(0.4, foe.reachMul - 0.0005);   // MUTANT\n")],
  # [5] "nothing else", at the second-hex insert: the lab's arm-B shrink, 12% a hit in the window, never restored
  "r4-shrinkhit": [("      self.unmakeTally.blows++;\n",
                    "      self.unmakeTally.blows++;\n      foe.reachMul = Math.max(0.4, foe.reachMul - 0.12);   // MUTANT\n")],
  # [2] "every stun a hex lands ... lasts twice as long" -- the LENGTH, not the rate: hexes proc twice as often in the window
  "r5-cadence": [("      f.hexClock += dt * hx;\n", "      f.hexClock += dt * hx * f.hexStunMul;   // MUTANT\n")],
}
outd.mkdir(parents=True, exist_ok=True)
for name, eds in M.items():
    s = base
    for a, b in eds: s = one(s, a, b)
    p = outd / f"sc-spellbreaker-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    print(name, hashlib.sha256(s.encode()).hexdigest()[:16])
