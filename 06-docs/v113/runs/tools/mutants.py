"""SCRATCH MUTANTS OF THE FINAL LINK (stage 5), each breaking ONE sentence of v84 in a way that changes
fights (m12 excepted, and said: a beat is read by the director only); each must fail its own probe check
and only that one (v113 §3). Probed with --stage 5.
    python mutants.py <final.html> <outdir> <blade>"""
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
BLADE = sys.argv[3]
def one(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:80])
    return s.replace(old, new, 1)
NL = chr(10)
CALL = "    if (self.ultBramble && (self === this.a || self === this.b)) this.plantBramble(self, foe);" + NL
M = {}
# [1] "for a duration": the window (and the brambles, and the thorns) on the lab's clock -- tickBramble on every frozen step too
TAG = "      this.tickBramble(dt);   // MUTANT m1" + NL
s = one(src, "      L.t += dt;\n      this.t += dt;\n", "      L.t += dt;\n      this.t += dt;\n" + TAG)
s = one(s, "      S.t += dt;\n      this.t += dt;\n", "      S.t += dt;\n      this.t += dt;\n" + TAG)
M["m1-window-labclock"] = (1, one(s, "      this.hitStop -= dt;\n      this.t += dt;\n", "      this.hitStop -= dt;\n      this.t += dt;\n" + TAG))
# [2] "every blow the scythe lands leaves a bramble": only every other blow in the window plants
M["m2-every-other-blow"] = (2, one(src, CALL, CALL.replace("this.plantBramble(self, foe);", "{ if (self.hits % 2 === 0) this.plantBramble(self, foe); }")))
# [3] "brambles outlive the window": the caster's brambles are cleared at the window's close
CLOSE = "        if (Z.t >= Z.dur || !f.alive || !foe.alive) f.ultBramble = null;" + NL
M["m3-cleared-at-close"] = (3, one(src, CLOSE, "        if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultBramble = null; "
                                  "for (let i = G.length - 1; i >= 0; i--) if (G[i].side === side) G.splice(i, 1); }" + NL))
# [3] "a patch r 80": the thorns reach 10 further than the bramble
M["m3b-radius-plus10"] = (3, one(src, "Math.hypot(foe.x - b.x, foe.y - b.y) < u.patchR + R)", "Math.hypot(foe.x - b.x, foe.y - b.y) < u.patchR + R + 10)"))
# [4] "rooted -- ball AND WEAPON": the snare frees the weapon (pinFree 1), so tickStasis does not lock it
PM = "            foe.pinMax = Math.max(foe.pinMax, u.rootFor);" + NL
M["m4-weapon-free"] = (4, one(src, PM, PM + "            foe.pinFree = 1;" + NL))
# [5] "entangled +1": +2 a bite
M["m5-entangle-2"] = (5, one(src, 'foe.apply("entangle", u.tickEnt, side);', 'foe.apply("entangle", u.tickEnt + 1, side);'))
# [6] "no hit stop": the bite stops the world 0.05s
TK = "          T.ticks++;" + NL
M["m6-bite-hitstop"] = (6, one(src, TK, TK + "          this.hitStop = Math.max(this.hitStop, 0.05);" + NL))
# [6] "no knock": the bite pushes the foe
M["m6b-bite-knock"] = (6, one(src, TK, TK + "          foe.vx += 60;" + NL))
# [8] the charge on the game's clock: the lab's 16 unconverted
M["m7-charge16"] = (8, one(src, 'ult:{ name:"Bramblesnare", charge:14, kind:"bramble"', 'ult:{ name:"Bramblesnare", charge:16, kind:"bramble"'))
# [4]+[8] THE STAGE'S OWN NUMBER LOST: the row's snare back at 0 (a link that lost its snare)
M["m8-row-no-snare"] = ((4, 8), one(src, "          rootFor:0.6,          // v84: the snare on entry (stage 3)",
                                        "          rootFor:0,          // v84: the snare on entry (stage 3)"))
# [8] THE STAGE'S OWN NUMBER LOST: the blade back at the shipped 31.35 (byte-identical to stage 3's link)
ROWB = '  { id:"thornwake", name:"Thornwake", aff:"verdant", shape:"scythe",\n    blades:[0], reach:104, width:11, artW:46, dmg:'
M["m9-blade-shipped"] = (8, one(src, ROWB + BLADE + ",", ROWB + "31.35,"))
# [4] "on ENTRY": the snare re-written on every inside frame
M["m10-snare-every-frame"] = (4, one(src, "        if (!f.brambleIn){" + NL, "        if (true){" + NL))
# [7] a killing bite files no beat -- DOES NOT CHANGE FIGHTS (a beat is the director's), a control for [7] only
M["m11-kill-no-beat"] = (7, one(src, "          if (wasUp && foe.hp <= 0){" + NL, "          if (false){" + NL))
for name, (k, s) in M.items():
    p = out / f"mut-{name}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    ks = ",".join(map(str, k)) if isinstance(k, tuple) else str(k)
    print(f"{name:<24} want [{ks}]  {hashlib.sha256(s.encode()).hexdigest()[:16]}  ({len(s) - len(src):+d} chars)")
