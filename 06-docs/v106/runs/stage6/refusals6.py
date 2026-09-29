"""Stage 6's builder refusals, each able to fail: run the real builder where it must refuse, and
scratch copies of it with one S6 row mutated (never the repo's file)."""
import pathlib, re, subprocess, sys
PY = "C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
B = pathlib.Path("C:/dev/sundered-crown/tools/widowmaker_build.py")
D = S / "s6" / "refuse"; D.mkdir(exist_ok=True)
base, fx, drain = S / "links/sc-widowmaker-b1075.html", S / "links/sc-widowmaker-b1075-fx.html", S / "links/sc-widowmaker-drain.html"
src = B.read_text(encoding="utf-8")

def run(builder, src_p, tag, want):
    out = D / f"sc-widowmaker-refuse-{tag}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(builder), "--stage", "6", "--src", str(src_p), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    msg = (r.stdout + r.stderr).strip().splitlines()
    last = [l for l in msg if "REFUS" in l or "stage 6 goes" in l or "already" in l or "wrong base" in l]
    ok = r.returncode != 0 and not out.exists() and any(want in l for l in msg)
    print(f"  {'REFUSED' if ok else 'NOT REFUSED -- FAIL'}  {tag:<22} rc {r.returncode}  {last[-1].strip() if last else msg[-1]}")
    return ok

def mutant(tag, old, new, count=1):
    assert src.count(old) == count, (tag, src.count(old))
    p = D / f"wb_{tag}.py"
    p.write_text(src.replace(old, new), encoding="utf-8", newline="\n")
    return p

res = []
print("REAL BUILDER:")
res.append(run(B, fx, "twice", "already in this source"))
res.append(run(B, drain, "on-stage2", "wrong base"))
print("MUTATED S6 ROWS (scratch copies of the builder):")
res.append(run(mutant("siphon-writes-sim", "        f.siphonHp = w;\n", "        f.siphonHp = w; foe.vx += 1e-9;\n"), base, "siphon-writes-sim", "writes foe.vx"))
res.append(run(mutant("drip-floats", '              SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") });',
                      '              { SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") }); this.float(me.x, me.y, "+1", "#f00", 30); }'),
               base, "drip-floats", "floats a number outside tickSiphon"))
res.append(run(mutant("siphon-rng", "shellHash(1931, w)", "this.rng()"), base, "siphon-rng", "draws the RNG"))
res.append(run(mutant("close-voice", "        f.siphonFade = 0;\n      }\n", '        f.siphonFade = 0; SFX.play("ult", { w: "widowmaker" });\n      }\n'),
               base, "close-voice", "plays a voice outside"))
res.append(run(mutant("slice-kept", "          const g = 0.5386;\n", "          const g = 0.5386; this._burst(t, { freq: 3400, q: 1.6, gain: 0.34, dur: 0.20 });\n"),
               base, "slice-kept", "wet slice is still here"))
print(f"\n{sum(res)}/{len(res)} refused as they must")
sys.exit(0 if all(res) else 1)
