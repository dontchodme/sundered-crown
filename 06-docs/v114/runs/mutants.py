"""v114 scratch: the probe's controls. Eleven mutants of the final link, each
breaking ONE sentence (or one declared reading) in a way that changes fights
(but [8], the lab's own shared-row method, which changes no fight the probe
plays: it is the control that [8] can fail). Each must fail its own check and
only that one. [10] is the build review's (2026-09-30) R2 (the foe's blows priced in her
window, by her own Hemorrhage), and [10b] its bracket arm (the same price keyed
on her relic, not her window: it reads no field of hers). `changed` counts fights
(Goreshard v every foe, 2 seeds, both sides) whose `AC.simulate` summary
differs from the unmutated link's. (v106's mutants.py, for this relic.)

    python mutants.py <final link> <out dir> <stage> [probe seeds] [only tags]
"""
import os, pathlib, re, subprocess, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

PY = sys.executable
link = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); stage = sys.argv[3]
seeds = sys.argv[4] if len(sys.argv) > 4 else "3"
only = sys.argv[5].split(",") if len(sys.argv) > 5 and sys.argv[5] != "all" else None
out.mkdir(parents=True, exist_ok=True)
src = link.read_text(encoding="utf-8")

M = [
 (1, "the window 10% long", [
   ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultPrice = null; continue; }",
    "      if (Z.t >= Z.dur * 1.1 || !f.alive || !foe.alive){ f.ultPrice = null; continue; }")]),
 (2, "the price read AFTER the blow's own onHit (the stacks it leaves, not the ones it found)", [
   ('    const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;',
    '    const priceN = self.ultPrice ? Math.min(4, foe.stacks("hemorrhage") + 2) : 0;')]),
 (3, "the struck fighter's bleed ceiling 8 while she prices (§6.3's Bloodletting cap)", [
   ("                 ? foe.w.ult.cap : STATUS.hemorrhage.maxStacks;",
    "                 ? foe.w.ult.cap : (foe.ultPrice ? 8 : STATUS.hemorrhage.maxStacks);")]),
 (8, "the lab's method: the shared row's dmg written at every blow of hers (changes no fight the probe plays: no mirror)", [
   ("    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n",
    "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n"
    "    if (self.w.id === \"oathwound\") self.w.dmg = 10.25 * (1 + 0.3 * priceN);   /* MUTANT: the lab's method, the shared row */\n"),
   ("self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : ", "self.ultPrice ? self.w.dmg : ")]),
 (4, "the price also with the window shut (after the first cast)", [
   ("self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : ",
    'self.priceTally ? self.w.dmg * (1 + self.w.ult.perStack * (self.ultPrice ? priceN : foe.stacks("hemorrhage"))) : ')]),
 (5, "the blade's reach +10% in the window", [
   ("       tests against, so the hit box and the drawn chain grow together. */\n"
    "    const reach = f.w.reach * mods.reach * f.reachMul;",
    "       tests against, so the hit box and the drawn chain grow together. */\n"
    "    const reach = f.w.reach * mods.reach * f.reachMul * (f.ultPrice ? 1.1 : 1);")]),
 (6, "the beam's 3 Hemorrhage kept at the cast", [
   ("      f.priceTally.casts++;\n      return;",
    "      f.priceTally.casts++; foe.apply(\"hemorrhage\", 3);\n      return;")]),
 (7, "the lab's charge 16, unconverted", [
   ('charge:14, kind:"price", dur:8,', 'charge:16, kind:"price", dur:8,')]),
 (9, "the window's ticker stops the world a little every window frame", [
   ("      f.priceTally.frames++;\n",
    "      f.priceTally.frames++; this.hitStop = Math.max(this.hitStop, 0.001);\n")]),
 ("10", "the foe's blows on her priced too while her window is open (the review's R2)", [
   ('    const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;',
    '    const priceN = (self.ultPrice || foe.ultPrice) ? foe.stacks("hemorrhage") : 0;'),
   ("self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : ",
    "(self.ultPrice || foe.ultPrice) ? self.w.dmg * (1 + 0.3 * priceN) : ")]),
 ("10b", "the foe's blows on her priced by her Hemorrhage, keyed on her relic, not her window (no field of hers read)", [
   ('    const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;',
    '    const priceN = (self.ultPrice || foe.w.id === "oathwound") ? foe.stacks("hemorrhage") : 0;'),
   ("self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : ",
    '(self.ultPrice || foe.w.id === "oathwound") ? self.w.dmg * (1 + 0.3 * priceN) : ')]),
]
NOFIGHT = {"8"}   # the declared control: the lab's method, bit-identical to the build (no mirror in the probe)

JS = r"""() => { const out = []; const ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "oathwound");
  for (const f of ids) for (const sd of [7001, 7013]){ out.push(AC.simulate("oathwound", f, sd)); out.push(AC.simulate(f, "oathwound", sd)); }
  return out; }"""


def fights(p):
    with game(game_path=p) as (page, errors):
        r = page.evaluate(JS); assert not errors, errors
    return r


ref = fights(link.resolve())
rows = []
for tag, what, edits in M:
    if only and str(tag) not in only:
        continue
    k = int(re.match(r"\d+", str(tag)).group(0))       # the check this mutant must fail, and only it
    s = src
    for a, b in edits:
        assert s.count(a) == 1, (tag, a)
        s = s.replace(a, b, 1)
    p = out / f"mut{tag}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    changed = sum(1 for x, y in zip(ref, fights(p.resolve())) if x != y)
    r = subprocess.run([PY, "goreshard_probe.py", "--game", str(p.resolve()), "--stage", stage, "--seeds", seeds],
                       cwd=r"C:/dev/sundered-crown/tools", capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    (out / f"mut{tag}.probe.txt").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    lines = r.stdout.splitlines()
    failed = [int(m.group(1)) for l in lines for m in [re.match(r"\s*\[(\d+)\] FAIL", l)] if m]
    score = next((l.strip() for l in lines if re.match(r"\s*\d+/\d+$", l)), "?")
    ok = failed == [k]
    first = next((l.strip() for l in lines if l.strip().startswith(f"[{k}] FAIL")), "")
    win = next((re.search(r"Goreshard win ([\d.]+%)", l).group(1) for l in lines if "Goreshard win" in l), "?")
    rows.append((tag, what, changed, failed, ok, first[:230]))
    print(f"mutant [{tag}] {what:<58} fights changed {changed:>3}/{len(ref)}   probe {score}  fails {failed}  "
          f"Goreshard wins {win}   {'OWN CHECK ONLY: PASS' if ok else 'FAIL'}\n    {first[:260]}", flush=True)
good = lambda r: r[4] and (r[2] > 0 or str(r[0]) in NOFIGHT)
allok = all(good(r) for r in rows)
print(f"\n{sum(1 for r in rows if good(r))}/{len(rows)} mutants fail their own check and only that one, and change fights "
      f"(but the declared no-fight control {sorted(NOFIGHT)})")
sys.exit(0 if allok else 1)
