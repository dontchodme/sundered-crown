"""v113 §1: THE BUILDER'S SCAN CAN FAIL. Copies of tools/thornwake_build.py, each with ONE forbidden line added
to tickBramble's insert (after `T.ticks++;`), run as stage 2 on the stub; every copy must REFUSE, before writing,
for the reason named. A final copy with nothing added must build the stage-2 link byte-identical (the control of
the control).    python builder_negatives.py <S> <want sha16 of stage 2>"""
import hashlib, pathlib, subprocess, sys
S = pathlib.Path(sys.argv[1]); WANT = sys.argv[2]; T = S / "tmp" / "neg"; T.mkdir(parents=True, exist_ok=True)
PY = sys.executable
src = pathlib.Path("C:/dev/sundered-crown/tools/thornwake_build.py").read_text(encoding="utf-8")
src = src.replace('HERE = pathlib.Path(__file__).parent', 'HERE = pathlib.Path("C:/dev/sundered-crown/tools")', 1)
AN = "          T.ticks++;\n"
assert src.count(AN) == 1
BAD = [
    ("knock the foe", "foe.vx = 0;", "writes foe.vx"),
    ("stun it", "foe.stun = Math.max(foe.stun, 1);", "stuns"),
    ("stop the world", "this.hitStop = Math.max(this.hitStop, 0.05);", "stops the world"),
    ("feed the charge", "f.charge += 1;", "writes f.charge"),
    ("a second status", 'foe.apply("burn", 1, side);', "applies"),
    ("hurt again", "this.hurt(foe, 1, f);", "hurts"),
    ("free the weapon", "foe.pinFree = 1;", "pinFree"),
    ("write the shared weapon", "f.w.dmg = 13;", "shared weapon"),
    ("draw the RNG", "const r0 = this.rng();", "RNG"),
    ("grow the reach", "foe.reachMul = 1;", "writes foe.reachMul"),
    ("file a second beat", 'this.beat({ kind: "ult" });', "beat"),
    ("write a status by hand", "foe.status.entangle.stacks = 4;", "writes entangle.stacks"),
    ("voice it", 'SFX.play("ult", { w: "thornwake-bite" });', "calls .play("),
    ("Math.random", "const r1 = Math.random();", "Math.random"),
    ("take the ultFx slot", "this.ultFx = null;", "ultFx"),
    ("delete a status", "delete foe.status.hex;", "deletes"),
    ("hitstun", "foe.takeHitstun(5);", "calls .takeHitstun("),
    ("move the ball", "foe.x += 1;", "writes foe.x"),
    ("heal the caster", "f.hp += 2;", "writes f.hp"),
    ("float a number", 'this.float(foe.x, foe.y, "2", "#fff", 20);', "calls .float("),
]
stub = S / "links" / "sc-thornwake-stub.html"
lines, ok = [], True
for i, (name, bad, why) in enumerate(BAD + [("CONTROL: nothing added", None, None)]):
    b = src if bad is None else src.replace(AN, AN + "          " + bad + "\n", 1)
    bp = T / f"thornwake_build_neg{i:02d}.py"; bp.write_text(b, encoding="utf-8", newline="\n")
    out = T / f"sc-thornwake-neg{i:02d}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(bp), "--stage", "2", "--src", str(stub), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    txt = (r.stdout + r.stderr)
    if bad is None:
        good = r.returncode == 0 and out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()[:16] == WANT
        lines.append(f"{name:<28} rc {r.returncode}  -> " + (f"BUILDS, byte-identical to sc-thornwake-bramble ({WANT})" if good else "!! " + txt[-200:]))
    else:
        refused = [l for l in txt.splitlines() if "REFUSING" in l]
        good = r.returncode != 0 and not out.exists() and bool(refused) and why in refused[0]
        lines.append(f"{name:<28} +{bad:<50} rc {r.returncode}  -> " + (f"REFUSED: {refused[0].split("' ", 1)[-1].strip()[:120]}" if good else "!! NOT REFUSED FOR THE REASON: " + txt[-240:].replace(chr(10), ' | ')))
    ok &= good
lines.append("")
lines.append(f"{len(BAD)} negative copies, every one refused for its reason; the unmodified copy builds the link" if ok else "!! THE SCAN MISSED ONE")
text = "\n".join(lines) + "\n"
(S / "runs" / "builder_negatives.txt").write_text(text, encoding="utf-8", newline="\n"); print(text)
