"""v106 stage 6, scratch: the probe's [11] and [12] must be able to fail. Mutants of the stage-6 link
(sc-widowmaker-b1075-fx.html), each breaking one stage-6 sentence; each must fail its own check and only
that one. The voice and thread mutants move no fight (presentation), so the probe must see them with
every fight identical; the sim-write mutant moves fights. CONTROLS: the unmutated link under the same
harness passes 12/12, and the stage-5 probe (widowmaker_probe.py before stage 6, 7c1e5d1420211714) passes
every mutant 10/10 -- it cannot see stage 6 at all, so [11]-[12] are what catch them.

    python mutants6.py <fx link> <out dir> [probe seeds]
"""
import os, pathlib, re, subprocess, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

PY = sys.executable
TOOLS = r"C:/dev/sundered-crown/tools"
CTL = str(pathlib.Path(__file__).parent / "probe_pre_s6_control.py")
link = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); seeds = sys.argv[3] if len(sys.argv) > 3 else "2"
out.mkdir(parents=True, exist_ok=True)
src = link.read_text(encoding="utf-8")

M = [
 ("0", None, "CONTROL: the stage-6 link unmutated", []),
 ("11a", 11, "the drip on every drain tick, not once per whole hp", [
   ("            if (Math.floor(me.drainTally.drained) > k0)\n",
    "            if (me.drainTally.drained > k0)\n")]),
 ("11b", 11, "a close voice, on a death only", [
   ("      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; continue; }",
    "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; "
    "if (!f.alive || !foe.alive) SFX.play(\"ult\", { w: \"widowmaker-drain\", n: 4 }); continue; }")]),
 ("12a", 12, "the picture's hook writes the sim (foe.vx += 1e-9 on a '+n')", [
   ("        f.siphonHp = w;\n", "        f.siphonHp = w; foe.vx += 1e-9;\n")]),
 ("12b", 12, "the thread left up past its close (no snap)", [
   ("      else if (f.siphonFade > 0){\n", "      else if (false){\n")]),
]

JS = r"""() => { const out = []; const ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "widowmaker");
  for (const f of ids) for (const sd of [7001, 7013]){ out.push(AC.simulate("widowmaker", f, sd)); out.push(AC.simulate(f, "widowmaker", sd)); }
  return out; }"""


def fights(p):
    with game(game_path=p) as (page, errors):
        r = page.evaluate(JS); assert not errors, errors
    return r


def probe(script, p):
    r = subprocess.run([PY, script, "--game", str(p.resolve()), "--seeds", seeds], cwd=TOOLS,
                       capture_output=True, text=True, encoding="utf-8",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    lines = r.stdout.splitlines()
    failed = [int(m.group(1)) for l in lines for m in [re.match(r"\s*\[(\d+)\] FAIL", l)] if m]
    score = next((l.strip() for l in lines if re.match(r"\s*\d+/\d+$", l)), "?")
    return r, failed, score, lines


ref = fights(link.resolve())
res = []
for tag, k, what, edits in M:
    s = src
    for a, b in edits:
        assert s.count(a) == 1, (tag, a)
        s = s.replace(a, b, 1)
    p = out / f"mut6_{tag}.html"
    p.write_text(s, encoding="utf-8", newline="\n")
    changed = sum(1 for x, y in zip(ref, fights(p.resolve())) if x != y)
    r, failed, score, lines = probe("widowmaker_probe.py", p)
    (out / f"mut6_{tag}.probe.txt").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    if k is None:
        ok = failed == [] and score == "12/12" and changed == 0
        print(f"[{tag}] {what:<62} fights changed {changed:>3}/{len(ref)}   probe {score}  fails {failed}   "
              f"{'CLEAN: PASS' if ok else 'FAIL'}", flush=True)
        res.append(ok)
        continue
    first = next((l.strip() for l in lines if l.strip().startswith(f"[{k}] FAIL")), "")
    ok = failed == [k]
    rc, cfailed, cscore, _ = probe(CTL, p)
    (out / f"mut6_{tag}.ctl.txt").write_text(rc.stdout + "\n" + rc.stderr, encoding="utf-8")
    cok = cfailed == [] and cscore == "10/10"
    print(f"[{tag}] {what:<62} fights changed {changed:>3}/{len(ref)}   probe {score}  fails {failed}   "
          f"{'OWN CHECK ONLY: PASS' if ok else 'FAIL'}   stage-5 probe {cscore} ({'blind, as it must be' if cok else 'NOT BLIND'})\n"
          f"    {first[:260]}", flush=True)
    res.append(ok and cok)
print(f"\n{sum(res)}/{len(res)} as they must be (the control clean; every mutant fails its own check alone, "
      f"and the stage-5 probe passes it)")
sys.exit(0 if all(res) else 1)
