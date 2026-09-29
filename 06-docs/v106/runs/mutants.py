"""v106 scratch: the probe's controls. Twenty-two mutants of the final link, each
breaking ONE sentence in a way that changes fights. Each must fail its own
check and only that one. `changed` counts fights (Widowmaker v every foe, 2
seeds, both sides) whose summary differs from the unmutated link's.

Round 1 (the first review): the two [5] mutants break "her blades are
unchanged" by the two routes a blow's damage can take, through `Fighter.dmgMul`
(the review's mutant D, which the first probe could not see) and in
`resolveHit`.
Round 2 (the second review): [1f] is the review's R1, the window ticking
through a hit stop (the lab's step clock), which the probe before round 2
passed 8/8; [9] is its R63, §6.3's real left-out option (the foe's
bleed ceiling lifted to Bloodletting's 8 while she drains), which it also
passed 8/8; [5o] and [4t] are its ROH and RFT, kept as controls of the [5]
onHit split and of [4]'s foe tick.
Round 3 (the third review): [5s] is its SPIN (her blades 10% faster in the
window), [10l] its LS (the rejected arm D, lifesteal 0.35 in the window) and
[10b] its BLESS (Blessing 3 on her at the cast), which the round-2 probe
passed 9/9. The rest close the same class of hole around them: the blade's
knock [5k], reach [5w] and clank mass [5c] in the window, a row edit of the
twinblade [5p], her own stun at the cast [6h], and the two numbers the probe
used to read from the row under test, the window [1d] and the charge [8c].

    python mutants.py <final link> <out dir> [probe seeds] [only tags]
"""
import json, pathlib, re, subprocess, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

PY = sys.executable
link = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); seeds = sys.argv[3] if len(sys.argv) > 3 else "3"
probe = sys.argv[5] if len(sys.argv) > 5 else "widowmaker_probe.py"
out.mkdir(parents=True, exist_ok=True)
src = link.read_text(encoding="utf-8")

M = [
 (1, "the window 10% long", [
   ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; continue; }",
    "      if (Z.t >= Z.dur * 1.1 || !f.alive || !foe.alive){ f.ultDrain = null; continue; }")]),
 ("1f", "the window also ticks in a hit stop (R1)", [
   ("      this.hitStop -= dt;\n      this.t += dt;\n",
    "      this.hitStop -= dt;\n      this.t += dt;\n      this.tickDrain(dt);   /* MUTANT: the lab's step clock */\n")]),
 (2, "the drain 1% over the tick", [
   ("            me.hp = Math.min(me.maxHp, me.hp + d);",
    "            me.hp = Math.min(me.maxHp, me.hp + d * 1.01);")]),
 (3, "the heal past maxHp (§2's cap lifted)", [
   ("            me.hp = Math.min(me.maxHp, me.hp + d);",
    "            me.maxHp = Math.max(me.maxHp, me.hp + d); me.hp = me.hp + d;")]),
 (4, "the drain with the window shut", [
   ("          if (me && me.ultDrain && me.alive",
    "          if (me && me.w.id === \"widowmaker\" && me.alive"),
   ("            me.drainTally.ticks++;\n            me.drainTally.drained += me.hp - h0;",
    "            if (me.drainTally){ me.drainTally.ticks++; me.drainTally.drained += me.hp - h0; }")]),
 ("4t", "the foe's bleed 10% harder in the window (RFT)", [
   ("        const d = def.dps * st.stacks * dt * f.dmgTakenMul();\n        f.hp -= d;\n",
    "        const d = def.dps * st.stacks * dt * f.dmgTakenMul();\n        f.hp -= d;\n"
    "        if (key === \"hemorrhage\" && (f === this.a ? this.b : this.a).ultDrain) f.hp -= 0.1 * d;   /* MUTANT */\n")]),
 ("5d", "blades +5% in the window, via dmgMul", [
   ("  dmgMul(actDmg){ return actDmg * (this.desperate ? CONFIG.desperation.dmg : 1); }",
    "  dmgMul(actDmg){ return actDmg * (this.desperate ? CONFIG.desperation.dmg : 1) * (this.ultDrain ? 1.05 : 1); }")]),
 ("5r", "blades +5% in the window, in resolveHit", [
   ("            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul();",
    "            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul() * (self.ultDrain ? 1.05 : 1);")]),
 ("5o", "her onHit bleed 3, not 2, in the window (ROH)", [
   ("      foe.apply(k, n);\n      const first = !this.taught[k] && !!(STATUS[k] && STATUS[k].tip);",
    "      foe.apply(k, n + (self.ultDrain && k === \"hemorrhage\" ? 1 : 0));\n      const first = !this.taught[k] && !!(STATUS[k] && STATUS[k].tip);")]),
 (6, "the nova's 3 hemorrhage kept at the cast", [
   ("      f.ultDrain = { t: 0, dur: u.dur };",
    "      f.ultDrain = { t: 0, dur: u.dur }; foe.apply(\"hemorrhage\", 3);")]),
 (7, "a drain tick stops the world", [
   ("            me.hp = Math.min(me.maxHp, me.hp + d);",
    "            me.hp = Math.min(me.maxHp, me.hp + d); this.hitStop = Math.max(this.hitStop, 0.02);")]),
 (9, "the foe's bleed ceiling 8 in the window (R63, §6.3)", [
   ("                 ? foe.w.ult.cap : STATUS.hemorrhage.maxStacks;",
    "                 ? foe.w.ult.cap : (foe.ultDrain ? 8 : STATUS.hemorrhage.maxStacks);")]),
 # ---- round 3
 ("1d", "the row's window 9, not the build's 8", [
   ('charge:14, kind:"drain", dur:8,', 'charge:14, kind:"drain", dur:9,')]),
 ("5s", "her blades spin 10% faster in the window (SPIN)", [
   ("    const spin = (f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)",
    "    const spin = (f.ultVine ? 0 : f.w.spin * (f.ultDrain ? 1.1 : 1)) * f.spinMul(mods.spin)")]),
 ("5k", "her blow's knock x1.2 in the window", [
   ("* (crit ? 1.5 : 1) * kMul;", "* (crit ? 1.5 : 1) * kMul * (self.ultDrain ? 1.2 : 1);")]),
 ("5w", "her blades' reach +10% in the window", [
   ('    const reach = f.w.reach * mods.reach * f.reachMul;\n    if (f.w.mode === "chain"){\n      const dx = f.headX - f.x',
    '    const reach = f.w.reach * mods.reach * f.reachMul * (f.ultDrain ? 1.1 : 1);\n    if (f.w.mode === "chain"){\n      const dx = f.headX - f.x')]),
 ("5c", "her mass x3 in a clank in the window", [
   ("    const mA = A.w.mass, mB = B.w.mass;",
    "    const mA = A.w.mass * (A.ultDrain ? 3 : 1), mB = B.w.mass * (B.ultDrain ? 3 : 1);")]),
 ("5p", "the row's reach 66, not the twinblade's 62", [
   ("reach:62, width:8, artW:30, dmg:10.75,", "reach:66, width:8, artW:30, dmg:10.75,")]),
 ("6h", "the cast stuns her 0.3 s", [
   ("      f.ultDrain = { t: 0, dur: u.dur };",
    "      f.ultDrain = { t: 0, dur: u.dur }; f.stun = Math.max(f.stun, 0.3);")]),
 ("8c", "the lab's charge 16, unconverted", [
   ('charge:14, kind:"drain", dur:8,', 'charge:16, kind:"drain", dur:8,')]),
 ("10l", "lifesteal 0.35 in the window: arm D, rejected (LS)", [
   ("      f.ultDrain = { t: 0, dur: u.dur };",
    "      f.ultDrain = { t: 0, dur: u.dur }; f.lifesteal = 0.35;"),
   ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; continue; }",
    "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; f.lifesteal = 0; continue; }")]),
 ("10b", "Blessing 3 on her at the cast (BLESS)", [
   ("      f.ultDrain = { t: 0, dur: u.dur };",
    "      f.ultDrain = { t: 0, dur: u.dur }; f.apply(\"blessing\", 3);")]),
]

JS = r"""() => { const out = []; const ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "widowmaker");
  for (const f of ids) for (const sd of [7001, 7013]){ out.push(AC.simulate("widowmaker", f, sd)); out.push(AC.simulate(f, "widowmaker", sd)); }
  return out; }"""

def fights(p):
    with game(game_path=p) as (page, errors):
        r = page.evaluate(JS); assert not errors, errors
    return r

ref = fights(link.resolve())
rows = []
only = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] != "all" else None
for tag, what, edits in M:
    if only and str(tag) not in only: continue
    k = int(re.match(r"\d+", str(tag)).group(0))       # the check this mutant must fail, and only it
    s = src
    for a, b in edits:
        assert s.count(a) == 1, (tag, a)
        s = s.replace(a, b, 1)
    p = out / f"mut{tag}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    changed = sum(1 for x, y in zip(ref, fights(p.resolve())) if x != y)
    r = subprocess.run([PY, probe, "--game", str(p.resolve()), "--seeds", seeds],
                       cwd=r"C:/dev/sundered-crown/tools" if probe == "widowmaker_probe.py" else None,
                       capture_output=True, text=True, encoding="utf-8")
    (out / f"mut{tag}.probe.txt").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    lines = r.stdout.splitlines()
    failed = [int(m.group(1)) for l in lines for m in [re.match(r"\s*\[(\d+)\] FAIL", l)] if m]
    score = next((l.strip() for l in lines if re.match(r"\s*\d+/\d+$", l)), "?")
    ok = failed == [k]
    first = next((l.strip() for l in lines if l.strip().startswith(f"[{k}] FAIL")), "")
    rows.append((tag, what, changed, failed, ok, first[:230]))
    print(f"mutant [{tag}] {what:<48} fights changed {changed:>3}/{len(ref)}   probe {score}  fails {failed}   "
          f"{'OWN CHECK ONLY: PASS' if ok else 'FAIL'}\n    {first[:230]}", flush=True)
allok = all(r[4] and r[2] > 0 for r in rows)
print(f"\n{sum(1 for r in rows if r[4] and r[2] > 0)}/{len(rows)} mutants fail their own check and only that one, and change fights")
sys.exit(0 if allok else 1)
