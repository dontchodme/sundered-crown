"""v112 §1: THE BUILDER'S SCAN CAN FAIL. Copies of tools/heartwood_build.py, each with ONE forbidden line added
to rootBlow's insert (after `T.rooted++;`; 18, then the v112 review's four and four more ways around a name list), run as stage 2 on the stub; every copy must REFUSE, before writing,
for the reason named. A final copy with nothing added must build the root link byte-identical (the control of
the control).    python builder_negatives.py <S>"""
import hashlib, pathlib, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = S / "tmp" / "neg"; T.mkdir(parents=True, exist_ok=True)
PY = sys.executable
src = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_build.py").read_text(encoding="utf-8")
AN = "    T.rooted++;\n"
# stage 6 (v112 §6) re-emits the line in its voice row: the first occurrence is S2's rootBlow, the one
# `.replace(AN, ..., 1)` below edits
assert src.count(AN) == 2 and src.index(AN) < src.index(chr(10) + "S6 = [" + chr(10))
BAD = [
    ("knock the held ball", "q.vx = 0;", "writes q.vx"),
    ("stun it", "q.stun = Math.max(q.stun, hold);", "stuns"),
    ("stop the world", "this.hitStop = Math.max(this.hitStop, 0.06);", "stops the world"),
    ("feed the charge", "f.charge += 1;", "writes f.charge"),
    ("a second status", 'q.apply("burn", 1, "a");', "applies"),
    ("hurt it", "this.hurt(q, 1, f);", "hurts"),
    ("free the weapon", "q.pinFree = 1;", "pinFree"),
    ("write the shared weapon", "f.w.dmg = 13;", "shared weapon"),
    ("draw the RNG", "const r0 = this.rng();", "RNG"),
    ("grow the reach", "q.reachMul = 1;", "writes q.reachMul"),
    ("file a beat", 'this.beat({ kind: "ult" });', "beat"),
    ("write a status by hand", "q.status.entangle.stacks = 4;", "writes entangle.stacks"),
    ("voice it", 'SFX.play("ult", { w: "heartwood-root" });', "calls SFX.play("),
    ("Math.random", "const r1 = Math.random();", "Math.random"),
    ("take the ultFx slot", "this.ultFx = null;", "ultFx"),
    ("delete a status", "delete q.status.hex;", "deletes"),
    ("hitstun", "q.takeHitstun(5);", "calls q.takeHitstun("),
    ("move the ball", "q.x += 1;", "writes q.x"),
    # THE v112 REVIEW'S FOUR (finding 2: they built with rc 0 under the old refusal list)
    ("spawn sparks (RNG + objects)", "this.spawnSpark(f, q.x, q.y);", "calls this.spawnSpark("),
    ("Object.assign a stun", "Object.assign(q, { stun: 2 });", "uses 'Object'"),
    ("end a split", "if (q.ultSplit) this.endSplit(q, true);", "calls this.endSplit("),
    ("detonate", "this.detonate(f, q);", "calls this.detonate("),
    # AND FOUR MORE WAYS AROUND A NAME LIST
    ("a bare function call", "hurtFoe(q, 1);", "calls hurtFoe("),
    ("a call through a bracket", 'q["takeHitstun"](5);', "uses ']('"),
    ("new", "const z0 = new Set();", "uses 'new'"),
    ("an arrow", "[q].forEach(g => g);", "uses '=>'"),
]
stub = S / "links" / "sc-heartwood-stub.html"
lines, ok = [], True
for i, (name, bad, why) in enumerate(BAD + [("CONTROL: nothing added", None, None)]):
    b = src if bad is None else src.replace(AN, AN + "    " + bad + "\n", 1)
    bp = T / f"heartwood_build_neg{i:02d}.py"; bp.write_text(b, encoding="utf-8", newline="\n")
    out = T / f"sc-heartwood-neg{i:02d}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(bp), "--stage", "2", "--src", str(stub), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    txt = (r.stdout + r.stderr)
    if bad is None:
        good = r.returncode == 0 and out.exists() and \
            hashlib.sha256(out.read_bytes()).hexdigest()[:16] == "22f403961e5203a6"
        lines.append(f"{name:<28} rc {r.returncode}  -> " + ("BUILDS, byte-identical to sc-heartwood-root (22f403961e5203a6)" if good else "!! " + txt[-200:]))
    else:
        refused = [l for l in txt.splitlines() if "REFUSING" in l]
        good = r.returncode != 0 and not out.exists() and bool(refused) and why in refused[0]
        lines.append(f"{name:<28} +{bad:<50} rc {r.returncode}  -> " + (f"REFUSED: {refused[0].strip()[:110]}" if good else "!! NOT REFUSED FOR THE REASON: " + txt[-240:].replace(chr(10), ' | ')))
    ok &= good
lines.append("")
lines.append(f"{len(BAD)} negative copies, every one refused for its reason; the unmodified copy builds the link" if ok else "!! THE SCAN MISSED ONE")
text = "\n".join(lines) + "\n"
(S / "runs" / "builder_negatives.txt").write_text(text, encoding="utf-8", newline="\n"); print(text)
