"""STAGE 6's GUARDS CAN FAIL: copies of lightkeeper_build.py, each with ONE forbidden thing written into a
stage-6 insert, run --stage 6 on sc-lightkeeper-bulwark-b9.5 -> each must REFUSE and write nothing. The
unmodified copy must write the link (e3f16bf01f0e2995). Scratch only (tmp/guard6)."""
import hashlib, pathlib, subprocess, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-"
                 "claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper")
PY = "C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
B = pathlib.Path("C:/dev/sundered-crown/tools/lightkeeper_build.py")
src = B.read_text(encoding="utf-8")
D = S / "tmp/guard6"
D.mkdir(parents=True, exist_ok=True)
BASE = S / "links/sc-lightkeeper-bulwark-b9.5.html"
TB = "      const T = f.wallTally;\n      if (!T) continue;                                          // <- zero burden\n"
VARIANTS = [
    ("a sim write (the foe nudged)", TB, TB + "      foe.x += 1e-9;\n"),
    ("an RNG draw", TB, TB + "      this.rng();\n"),
    ("the one ultFx slot", "    const c = this.ctx, R = CONFIG.physics.ballR;\n",
     "    const c = this.ctx, R = CONFIG.physics.ballR, uf = m.ultFx;\n"),
    ("a beat (in the gong row)", '      SFX.play("ult", { w: "lightkeeper-gong" });' + "'''),",
     '      SFX.play("ult", { w: "lightkeeper-gong" }); this.beat({ kind: "hit" });' + "'''),"),
    ("a hurt", TB, TB + "      this.hurt(foe, 1, f);\n"),
    ("a status laid (stun)", TB, TB + '      foe.apply("stun", 1, "a");\n'),
    ("a splice of the shots in the air", "      P.length = 0;\n", "      P.length = 0;\n      this.shots.splice(0, 1);\n"),
    ("an index write into the shots", "    c.save();\n    c.beginPath();\n    c.rect(-4000, -4000, 8000, 8000);\n",
     "    c.save();\n    m.shots[0] = null;\n    c.beginPath();\n    c.rect(-4000, -4000, 8000, 8000);\n"),
    ("a write to the tally", "      S[0] = T.blocks; S[1] = T.arrows; S[2] = T.banked;\n",
     "      S[0] = T.blocks; S[1] = T.arrows; S[2] = T.banked; T.blocks++;\n"),
    ("Math.random", "      const h1 = shellHash(7717 + f.side, n * 16 + j)",
     "      const h0 = Math.random(), h1 = shellHash(7717 + f.side, n * 16 + j)"),
    ("a shared table through an alias (P = AFFINITIES.vigil)",
     "    const c = this.ctx, u = f.w.ult, P = AFFINITIES.vigil, R = CONFIG.physics.ballR;\n",
     "    const c = this.ctx, u = f.w.ult, P = AFFINITIES.vigil, R = CONFIG.physics.ballR;\n    P.core = \"#FFFFFF\";\n"),
    ("the shared weapon (w.reach)", TB, TB + "      f.w.reach = 116;\n"),
    ("a sim write in a draw method (the match's clock)",
     "    if (!(m.a.bulwarkFade > 0) && !(m.b.bulwarkFade > 0)) return;\n",
     "    if (!(m.a.bulwarkFade > 0) && !(m.b.bulwarkFade > 0)) return;\n    m.t += 0;\n"),
]
print(f"# neg_test6  builder {hashlib.sha256(src.encode()).hexdigest()[:16]}  base {BASE.name}")
nfail = 0
for i, (what, old, new) in enumerate([("the unmodified builder", None, None)] + VARIANTS):
    t = src if old is None else src.replace(old, new, 1)
    if old is not None and (src.count(old) != 1 or t == src):
        print(f"SETUP {what}: the anchor occurs {src.count(old)}x in the builder"); nfail += 1; continue
    bp = D / f"lk_build_v{i}.py"
    bp.write_text(t, encoding="utf-8", newline="\n")
    out = D / f"sc-lightkeeper-g{i}.html"
    if out.exists():
        out.unlink()
    r = subprocess.run([PY, str(bp), "--stage", "6", "--src", str(BASE), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    last = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip() and not ln.strip().startswith("ok")][-1:]
    if old is None:
        h = hashlib.sha256(out.read_bytes()).hexdigest()[:16] if out.exists() else None
        good = r.returncode == 0 and h == "e3f16bf01f0e2995"
        print(f"{'ok  ' if good else 'FAIL'}  {what} writes {h}")
    else:
        good = r.returncode != 0 and not out.exists()
        print(f"{'ok  ' if good else 'FAIL'}  {what}: {'REFUSES' if good else 'WROTE'} -- {last[0].strip() if last else ''}")
    nfail += not good
print(f"# neg_test6: {nfail} FAIL")
sys.exit(1 if nfail else 0)
