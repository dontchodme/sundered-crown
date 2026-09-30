"""v114 scratch: stage 6's mutants against the probe's [11]-[12]. For each mutant of the fx link
(tools/mutants6.py): the fights it changes (Goreshard v every foe, 2 seeds, both sides: `AC.simulate`'s
summary against the fx link's; a voice or a picture that moves no fight changes none, and the drawn-frame
mutant can only move a DRAWN fight), and the probe at 1 seed (--stage 6; the drawn mutant with --drawn 24).
Each must fail its own check, and only that one.

    python mutant_table6.py [only names, comma-separated]
"""
import os, pathlib, re, subprocess, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard")
FX = W / "links" / "sc-goreshard-b10.25-fx.html"
MD = W / "mutants6"
PY = sys.executable
only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
MUT = [("mV1-closevoice", 11, 0, "the cast voice again at every window close, a death's included (a close voice)"),
       ("mV2-x1priced", 11, 0, "the priced voice on every window blow, x1 ones included (price 0)"),
       ("mP1-picwrite", 12, 0, "tickGore nudges the foe's velocity 1e-9 at every mote it sheds (a sim write)"),
       ("mP2-glowfloor", 12, 0, "the glow's floor 0.25, not v81's 0.2"),
       ("mP3-floatx2", 12, 0, "the priced float x(1 + 0.2 n), not x(1 + 0.1 n)"),
       ("mP4-windowonly", 12, 0, "the red read off the window alone: held through the verdict when the kill leaves it set"),
       ("mD1-drawwrite", 12, 24, "the blade's draw writes the caster's velocity (a drawn frame only)")]
JS = r"""() => { const out = []; const ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "oathwound");
  for (const f of ids) for (const sd of [7001, 7013]){ out.push(AC.simulate("oathwound", f, sd)); out.push(AC.simulate(f, "oathwound", sd)); }
  return out; }"""


def fights(p):
    with game(game_path=p) as (page, errors):
        r = page.evaluate(JS); assert not errors, errors
    return r


ref = fights(FX.resolve())
rows = []
for name, k, drawn, what in MUT:
    if only and name not in only:
        continue
    p = MD / f"sc-goreshard-{name}.html"
    changed = sum(1 for x, y in zip(ref, fights(p.resolve())) if x != y)
    cmd = [PY, "goreshard_probe.py", "--game", str(p.resolve()), "--stage", "6", "--seeds", "1"]
    if drawn:
        cmd += ["--drawn", str(drawn)]
    r = subprocess.run(cmd, cwd=r"C:/dev/sundered-crown/tools", capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    (MD / f"{name}.probe.txt").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    lines = r.stdout.splitlines()
    failed = [int(m.group(1)) for l in lines for m in [re.match(r"\s*\[(\d+)\] FAIL", l)] if m]
    score = next((l.strip() for l in lines if re.match(r"\s*\d+/\d+$", l)), "?")
    ok = failed == [k]
    first = next((l.strip() for l in lines if l.strip().startswith(f"[{k}] FAIL")), "")
    nf = re.search(r"(\d+) FAIL", first)
    win = next((re.search(r"Goreshard win ([\d.]+%)", l).group(1) for l in lines if "Goreshard win" in l), "?")
    rows.append((name, k, changed, failed, ok))
    print(f"{name:<16} [{k}]{' drawn' if drawn else ''}  {what}\n    fights changed {changed:>3}/{len(ref)}   probe {score}  "
          f"fails {failed}  Goreshard wins {win}   {'OWN CHECK ONLY: PASS' if ok else 'FAIL'}\n    {first[:300]}", flush=True)
allok = all(r[4] for r in rows)
print(f"\n{sum(1 for r in rows if r[4])}/{len(rows)} stage-6 mutants fail their own check and only that one")
sys.exit(0 if allok else 1)
