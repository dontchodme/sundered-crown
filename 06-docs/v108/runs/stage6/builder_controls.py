"""v108 stage 6: the builder's own guards must be able to fail. Each control is a copy of
tools/ironhail_build.py with ONE forbidden thing written into a stage-6 insert; each must REFUSE
(exit 1, nothing written). The last control is the unmodified builder, which must write."""
import pathlib, subprocess, shutil, hashlib
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail")
PY = r"C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
B = pathlib.Path("C:/dev/sundered-crown/tools/ironhail_build.py").read_text(encoding="utf-8")
T = S / "s6/tmp/bctl"; shutil.rmtree(T, ignore_errors=True); T.mkdir(parents=True)
HOOK = "      f.quarrelSeen[0] = T.landed; f.quarrelSeen[1] = T.missed;\n"
DRAW = "    for (const q of FA) this._quarrelSplash(c, q, D);\n"
assert B.count(HOOK) == 1 and B.count(DRAW) == 1
CTL = [
    ("sim-write", HOOK, HOOK + "      foe.x += 1e-9;\n"),
    ("rng", HOOK, HOOK + "      const zz = this.rng();\n"),
    ("ultFx", HOOK, HOOK + "      if (this.ultFx) f.quarrelFade = 1;\n"),
    ("beat", HOOK, HOOK + "      this.beat({ kind: \"hit\" });\n"),
    ("splice-bolts", HOOK, HOOK + "      if (this.hail.length > 9) this.hail.splice(0, 1);\n"),
    ("bolt-index-write", DRAW, DRAW + "    if (m.hail.length) m.hail[0] = m.hail[0];\n"),
    ("tally-write", HOOK, HOOK + "      T.landed = T.landed;\n"),
    ("math-random", DRAW, DRAW + "    const jj = Math.random();\n"),
]
for name, a, b in CTL + [("none (the builder as it is)", HOOK, HOOK)]:
    p = T / f"ironhail_build_{name.split()[0]}.py"
    p.write_text(B.replace(a, b, 1), encoding="utf-8", newline="\n")
    out = T / f"sc-ironhail-ctl-{name.split()[0]}.html"
    r = subprocess.run([PY, str(p), "--stage", "6", "--src", str(S / "links/sc-ironhail-sunder.html"), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    last = (r.stdout + r.stderr).strip().splitlines()[-1]
    wrote = out.exists()
    print(f"  {name:<28} exit {r.returncode}  wrote {'YES' if wrote else 'no '}  | {last[:120]}")
