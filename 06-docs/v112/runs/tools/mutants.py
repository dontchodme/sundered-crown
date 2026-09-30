"""SCRATCH MUTANTS OF THE FINAL LINK (sc-heartwood-b11, stage 5), each breaking ONE sentence of v85 in a way
that changes fights; each must fail its own probe check and only that one (v112 §3). Probed with --stage 5.
    python mutants.py <final.html> <outdir>"""
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:80])
    return s.replace(old, new, 1)
CALL = "    if (self.ultRoot && (self === this.a || self === this.b)) this.rootBlow(self);\n"
KNOCK = "    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;\n"
M = {}
# [1] "for a duration": the window on the lab's clock -- tickRootfast also ticks on every frozen step
TAG = "      this.tickRootfast(dt);   // MUTANT m1\n"
s = one(src, "      L.t += dt;\n      this.t += dt;\n", "      L.t += dt;\n      this.t += dt;\n" + TAG)
s = one(s, "      S.t += dt;\n      this.t += dt;\n", "      S.t += dt;\n      this.t += dt;\n" + TAG)
M["m1-window-labclock"] = (1, one(s, "      this.hitStop -= dt;\n      this.t += dt;\n", "      this.hitStop -= dt;\n      this.t += dt;\n" + TAG))
# [2] "every blow the sword lands roots": only every other blow in the window roots
M["m2-every-other-blow"] = (2, one(src, CALL, CALL.replace("this.rootBlow(self);", "{ if (self.hits % 2 === 0) this.rootBlow(self); }")))
# [3] "the knock is applied and THEN frozen by the pin": the root written BEFORE the knock (pinV the pre-knock vector)
KN = "                * (crit ? 1.5 : 1) * kMul;\n" + KNOCK
M["m3-pin-before-knock"] = (3, one(one(src, CALL, ""), KN, KN.replace(KNOCK, CALL + KNOCK)))
# [4] "ball AND WEAPON": the root frees the weapon (pinFree 1), so tickStasis does not lock it
M["m4-weapon-free"] = (4, one(src, "    q.pinMax = Math.max(q.pinMax, hold);\n", "    q.pinMax = Math.max(q.pinMax, hold);\n    q.pinFree = 1;\n"))
# [5] "entangle +1 on top of the channel's 2": +2
M["m5-entangle-2"] = (5, one(src, 'q.apply("entangle", u.extraEnt, f === this.a ? "a" : "b");',
                              'q.apply("entangle", u.extraEnt + 1, f === this.a ? "a" : "b");'))
# [6] "no damage change ... nothing else": the root stops the world (Paradox's pin's 0.06 hit stop)
M["m6-root-hitstop"] = (6, one(src, "    T.rooted++;\n", "    T.rooted++;\n    this.hitStop = Math.max(this.hitStop, 0.06);\n"))
# [7] "Charge 15" on the game's clock: the lab's 16 unconverted
M["m7-charge16"] = (7, one(src, 'ult:{ name:"Rootfast", charge:13, kind:"rootfast"', 'ult:{ name:"Rootfast", charge:16, kind:"rootfast"'))
# THE REVIEW'S SHAPES (v111's adversarial review, applied here): a link that LOST A NUMBER, and writes the old
# fixed-field probe did not watch. Each is a control for the probe's fix, and the old probe (v1) passes all three.
# [5]+[7] the row lost its entangle (extraEnt 1 -> 0): behaviour and row both wrong, the stage pinned catches both
M["m8-row-no-entangle"] = ((5, 7), one(src, "          extraEnt:1,          // v85: the entangle (stage 3)",
                                            "          extraEnt:0,          // v85: the entangle (stage 3)"))
# [6] the root also resets the victim's stun diminishing returns (a field outside the old probe's list)
NL = chr(10)
M["m9-root-stundr"] = (6, one(src, "    q.pinMax = Math.max(q.pinMax, hold);" + NL,
                              "    q.pinMax = Math.max(q.pinMax, hold);" + NL + "    q.stunDR = 0;" + NL))
# [6] the window's ticker resets the caster's stun diminishing returns every frame
M["m10-ticker-stundr"] = (6, one(src, "      f.rootTally.frames++;" + NL,
                                 "      f.rootTally.frames++;" + NL + "      f.stunDR = 0;" + NL))
# [7] THE STAGE'S OWN NUMBER LOST: the blade back at the shipped 12.65 (byte-identical to stage 3's link)
ROWB = 'mode:"swing", arc:1.5, mass:3.0, dmg:'
M["m11-blade-shipped"] = (7, one(src, ROWB + "11,", ROWB + "12.65,"))
for name, (k, s) in M.items():
    p = out / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    ks = ",".join(map(str, k)) if isinstance(k, tuple) else str(k)
    print(f"{name:<24} want [{ks}]  {hashlib.sha256(s.encode()).hexdigest()[:16]}  ({len(s) - len(src):+d} chars)")
