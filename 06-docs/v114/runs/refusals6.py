"""v114 scratch: stage 6's refusals, each one able to fail (the stage 1-5 set is refusals.py).

(1) the stage-6 guards, on the real builder;
(2) NEGATIVE COPIES: the builder with ONE stage-6 row made wrong (a sim write, an RNG draw, the
    ultFx slot, a voice or float off its line, the fx.js copy touched, the fallback dropped ...),
    each of which the stage-6 scans must refuse. A copy that WRITES is a hole in the scan;
(3) the harness can pass: the builder copied unchanged writes the fx link's bytes, and a copy with
    a harmless change (a comment inside a row) writes too.
Every run writes to a temp folder and nothing is kept.
"""
import hashlib, pathlib, subprocess, sys, tempfile
T = pathlib.Path(r"C:/dev/sundered-crown/tools"); BASE = pathlib.Path(r"C:/dev/sundered-crown/02-chain/sc-tendril-t3.html")
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard")
L = W / "links"
STUB, PRICE, B5, FX = (L / "sc-goreshard-stub.html", L / "sc-goreshard-price.html",
                       L / "sc-goreshard-b10.25.html", L / "sc-goreshard-b10.25-fx.html")
PY = sys.executable
SRC = (T / "goreshard_build.py").read_text(encoding="utf-8")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:16]
FX_SHA = sha(FX)


def run(builder, stage, src, out):
    r = subprocess.run([PY, str(builder), "--stage", stage, "--src", str(src), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    msg = [l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    why = [l for l in msg if l.startswith(("REFUSING", "refusing", "wrong base", "ANCHOR", "BLOCK", "'", "stage ", "a link", "no such"))]
    return r.returncode, (why[0] if why else msg[-1] if msg else ""), out.exists()


FX_OLD = """    oathwound: { mode: 'beam', n: 1250, sp: [25, 140], grav: -60, drag: 1.3,
                 life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
                 spawn: 0.50, up: 0 },
"""
ok_all = True
with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d)
    B = T / "goreshard_build.py"
    guards = [
        ("stage 6 on the base", B, "6", BASE, d / "sc-goreshard-y1.html"),
        ("stage 6 on stage 2 (no blade under it)", B, "6", PRICE, d / "sc-goreshard-y2.html"),
        ("stage 6 on stage 6 (twice)", B, "6", FX, d / "sc-goreshard-y3.html"),
        ("stage 5 on stage 6", B, "5", FX, d / "sc-goreshard-y4.html"),
        ("stage 6 over an existing link", B, "6", B5, FX),
    ]
    print("(1) the stage-6 guards")
    for what, b, st, src, out in guards:
        existed = out.exists()
        rc, last, exists = run(b, st, src, out)
        good = rc != 0 and (exists == existed) and (not existed or sha(out) == FX_SHA)
        ok_all &= good
        print(f"  {'REFUSES' if good else 'WROTE!!'}  {what:<44} -> {last[:120]}")
    NEG = [
        ("tickGore writes the foe's velocity", "        f.goreAcc += dt * 5;\n",
         "        f.goreAcc += dt * 5; foe.vx += 1e-9;\n"),
        ("tickGore draws the match's RNG", "        f.goreAcc += dt * 5;\n",
         "        f.goreAcc += dt * 5 + 0 * this.rng();\n"),
        ("tickGore closes the window", "        f.goreFade = 1; f.goreOut = 0;\n",
         "        f.goreFade = 1; f.goreOut = 0; f.ultPrice = null;\n"),
        ("tickGore writes a status", "        f.goreFade = 1; f.goreOut = 0;\n",
         "        f.goreFade = 1; f.goreOut = 0; foe.status.hemorrhage.t = 0;\n"),
        ("tickGore turns the blade", "        f.goreTh = f.theta; f.goreT = this.t;\n",
         "        f.goreTh = f.theta; f.goreT = this.t; f.theta += 0;\n"),
        ("tickGore calls into the simulation (a note)", "          f.goreAcc -= 1;\n",
         "          f.goreAcc -= 1; this.note(\"blood\");\n"),
        ("tickGore plays a voice (off its line)", "          f.goreAcc -= 1;\n",
         "          f.goreAcc -= 1; SFX.play(\"hit\", { dmg: 1, crit: false });\n"),
        ("tickGore pushes a float", "          f.goreAcc -= 1;\n",
         "          f.goreAcc -= 1; this.floats.push({ x: 0, y: 0, text: \"\", c: \"#fff\", life: 1, size: 1 });\n"),
        ("tickGore assigns into the fighter", "          f.goreAcc -= 1;\n",
         "          f.goreAcc -= 1; Object.assign(f, { vx: 0 });\n"),
        ("the mote writes the shared weapon", "    const bh = f.w.artW * 0.19, n = f.goreDropN++, j = n % 5;\n",
         "    const bh = f.w.artW * 0.19, n = f.goreDropN++, j = n % 5; f.w.reach = 120;\n"),
        ("the motes' draw takes the ultFx slot", "    if (!a.goreDrops.length && !b.goreDrops.length) return;   // <- zero burden\n",
         "    if (!a.goreDrops.length && !b.goreDrops.length) return;   // <- zero burden\n    if (m.ultFx) return;\n"),
        ("the motes' draw uses Math.random", "        const r = 1.7 + 0.9 * shellHash(8123 + f.side, q.n), st = Math.min(5, sp * 0.012);\n",
         "        const r = 1.7 + 0.9 * Math.random(), st = Math.min(5, sp * 0.012);\n"),
        ("the motes' draw writes a module table", "    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;\n",
         "    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0; CONFIG.arena.w = 540;\n"),
        ("the float row is not its own text (x0.2)", "    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);\n'''),",
         "    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.2 * priceN);\n'''),"),
        ("the priced voice on every window blow (n >= 0)", "    if (priceN > 0) SFX.play(\"hit\", { dmg, crit, price: priceN });\n    else\n",
         "    if (priceN >= 0) SFX.play(\"hit\", { dmg, crit, price: priceN });\n    else\n"),
        ("the cast arm drops the rune-crack fallback", "type:\"sine\" });\n        } else {                                        // rune-crack'''),",
         "type:\"sine\" });\n        } else {'''),"),
        ("a row takes SPECS.oathwound out of the inlined fx.js", "\n]\n\n# THE STAGE-6 SCANS",
         "\n('bloodprice picture: fx out',\n '''" + FX_OLD + "''',\n ''''''),\n]\n\n# THE STAGE-6 SCANS"),
    ]
    print("(2) negative copies of the builder: one stage-6 row made wrong, each must refuse (stage 6 on the b10.25 link)")
    for i, (what, a, b) in enumerate(NEG):
        assert SRC.count(a) == 1, (what, SRC.count(a), a)
        nb = d / f"neg6_{i}_goreshard_build.py"
        nb.write_text(SRC.replace(a, b, 1), encoding="utf-8")
        out = d / f"sc-goreshard-neg6-{i}.html"
        rc, last, exists = run(nb, "6", B5, out)
        good = rc != 0 and not exists
        ok_all &= good
        print(f"  {'REFUSES' if good else 'WROTE!!'}  {what:<54} -> {last[:130]}")
    print("(3) the harness can pass")
    nb = d / "same_goreshard_build.py"
    nb.write_text(SRC, encoding="utf-8")
    out = d / "sc-goreshard-same-fx.html"
    rc, last, exists = run(nb, "6", B5, out)
    good = rc == 0 and exists and sha(out) == FX_SHA
    ok_all &= good
    print(f"  {'WRITES ' if good else 'FAILED!'}  the builder unchanged: {sha(out) if exists else '-'} (the fx link {FX_SHA})")
    a = "        f.goreAcc += dt * 5;\n"
    nb = d / "harmless_goreshard_build.py"
    nb.write_text(SRC.replace(a, "        f.goreAcc += dt * 5;             /* a harmless comment */\n", 1), encoding="utf-8")
    out = d / "sc-goreshard-harmless-fx.html"
    rc, last, exists = run(nb, "6", B5, out)
    good = rc == 0 and exists and sha(out) != FX_SHA
    ok_all &= good
    print(f"  {'WRITES ' if good else 'FAILED!'}  a harmless comment in tickGore: {sha(out) if exists else '-'} ({last[:60]})")
print(f"\n{'ALL REFUSE (and the harness passes the clean builder)' if ok_all else 'A HOLE: some run wrote, or the clean one did not'}")
sys.exit(0 if ok_all else 1)
