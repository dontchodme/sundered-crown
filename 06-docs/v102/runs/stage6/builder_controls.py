"""v102 stage 6: the builder's own guards must be able to fail. Each control is a copy of
tools/lodestone_build.py with ONE forbidden thing written into a stage-6 insert; each must REFUSE
(exit 1, nothing written). The last control is the unmodified builder, which must write."""
import pathlib, subprocess, shutil, hashlib
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone")
PY = r"C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
B = pathlib.Path("C:/dev/sundered-crown/tools/lodestone_build.py").read_text(encoding="utf-8")
T = S / "s6/tmp/bctl"; shutil.rmtree(T, ignore_errors=True); T.mkdir(parents=True)
HOOK = "        f.lodeSeen = T.touches;\n"                                   # tickLode, the touch
DRAW = "      this._lodeBolt(m, f, lodeHall(m.inset || 0), f.aff);\n"       # drawLodeTop
VOICE = '        SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });\n'   # tickRunes, the touch voice
assert B.count(HOOK) == 1 and B.count(DRAW) == 1 and B.count(VOICE) == 1
CTL = [
    ("sim-write", HOOK, HOOK + "        foe.x += 1e-9;\n"),
    ("rng", HOOK, HOOK + "        const zz = this.rng();\n"),
    ("ultFx", HOOK, HOOK + "        if (this.ultFx) f.lodeFade = 1;\n"),
    ("beat", HOOK, HOOK + '        this.beat({ kind: "hit" });\n'),
    ("apply", HOOK, HOOK + '        foe.apply("hex", 1, "a");\n'),
    ("tally-write", HOOK, HOOK + "        T.touches = T.touches;\n"),
    ("window-write", VOICE, VOICE + "        Z.cd = 0;\n"),
    ("tags-splice", DRAW, DRAW + "      m.tags.splice(0, 1);\n"),
    ("beats-index-write", DRAW, DRAW + "      if (m.beats.length) m.beats[0] = m.beats[0];\n"),
    ("math-random", DRAW, DRAW + "      const jj = Math.random();\n"),
]
for name, a, b in CTL + [("none (the builder as it is)", HOOK, HOOK)]:
    p = T / f"lodestone_build_{name.split()[0]}.py"
    p.write_text(B.replace(a, b, 1), encoding="utf-8", newline="\n")
    out = T / f"sc-lodestone-ctl-{name.split()[0]}.html"
    r = subprocess.run([PY, str(p), "--stage", "6", "--src", str(S / "links/sc-lodestone-b205.html"), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    last = (r.stdout + r.stderr).strip().splitlines()[-1]
    wrote = out.exists()
    sh = hashlib.sha256(out.read_bytes()).hexdigest()[:16] if wrote else ""
    print(f"  {name:<28} exit {r.returncode}  wrote {'YES ' + sh if wrote else 'no '}  | {last[:120]}")
