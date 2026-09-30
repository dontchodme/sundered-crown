"""v114 scratch: the builder's refusals, each one able to fail.

(1) the stage guards and the link rules, on the real builder;
(2) NEGATIVE COPIES: the builder with ONE insert made wrong (a write, a call,
    an RNG draw, a stop, a status, the order of the read), each of which the
    insert scan must refuse. A copy that WRITES is a hole in the scan.
Every run writes to a temp folder and nothing is kept.
"""
import pathlib, shutil, subprocess, sys, tempfile
T = pathlib.Path(r"C:/dev/sundered-crown/tools"); BASE = pathlib.Path(r"C:/dev/sundered-crown/02-chain/sc-tendril-t3.html")
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard")
STUB, PRICE = W / "links" / "sc-goreshard-stub.html", W / "links" / "sc-goreshard-price.html"
PY = sys.executable
SRC = (T / "goreshard_build.py").read_text(encoding="utf-8")


def run(builder, stage, src, out):
    r = subprocess.run([PY, str(builder), "--stage", stage, "--src", str(src), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    msg = [l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return r.returncode, (msg[-1] if msg else ""), out.exists()


ok_all = True
with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d)
    B = T / "goreshard_build.py"
    guards = [
        ("stage 2 on the base (no stub under it)", B, "2", BASE, d / "sc-goreshard-x1.html"),
        ("stage 1 on the stub (built already)", B, "1", STUB, d / "sc-goreshard-x2.html"),
        ("stage 2 on stage 2 (twice)", B, "2", PRICE, d / "sc-goreshard-x3.html"),
        ("stage 5 on the stub (no price under it)", B, "5", STUB, d / "sc-goreshard-x4.html"),
        ("a link that exists (overwrite)", B, "1", BASE, STUB),
        ("a name that is not sc-goreshard*", B, "1", BASE, d / "sc-other.html"),
        ("the live build's name", B, "1", BASE, d / "sundered-crown.html"),
    ]
    print("(1) the stage guards and the link rules")
    for what, b, st, src, out in guards:
        existed = out.exists()
        rc, last, exists = run(b, st, src, out)
        good = rc != 0 and (exists == existed)
        ok_all &= good
        print(f"  {'REFUSES' if good else 'WROTE!!'}  {what:<44} -> {last[:110]}")
    NEG = [
        ("tickPrice writes the foe's velocity", "      f.priceTally.frames++;\n",
         "      f.priceTally.frames++; foe.vx += 1e-9;\n"),
        ("the read draws the RNG", '    const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;',
         '    const priceN = self.ultPrice ? foe.stacks("hemorrhage") + 0 * this.rng() : 0;'),
        ("the cast writes the shared weapon", "      f.ultPrice = { t: 0, dur: u.dur };\n",
         "      f.ultPrice = { t: 0, dur: u.dur }; f.w.dmg = 12;\n"),
        ("the cast keeps the beam's bleed (an apply)", "      f.priceTally.casts++;\n      return;",
         "      f.priceTally.casts++; foe.apply(\"hemorrhage\", 3);\n      return;"),
        ("tickPrice stops the world", "      f.priceTally.frames++;\n",
         "      f.priceTally.frames++; this.hitStop = Math.max(this.hitStop, 0.01);\n"),
        ("the read floats a number", "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n",
         "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; this.float(foe.x, foe.y, 1, \"#fff\", 20); }\n"),
        ("the read heals the caster", "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n",
         "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; self.hp += 1; }\n"),
        ("the cast stuns the foe", "      f.ultPrice = { t: 0, dur: u.dur };\n",
         "      f.ultPrice = { t: 0, dur: u.dur }; foe.stun = 0.2;\n"),
        ("the read writes a status by index", "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n",
         "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; foe.status[\"hemorrhage\"] = null; }\n"),
        ("the read rewrites the jitter", "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n",
         "    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }\n    jitter = 1;\n"),
        ("tickPrice calls into the simulation (hurt)", "      f.priceTally.frames++;\n",
         "      f.priceTally.frames++; this.hurt(foe, 0, f);\n"),
        ("the price read from the stacks AFTER the onHit (the read moved below the damage line)",
         "PRICE_READ_ANCHOR = '''    const jitter = 1 + (this.rng() - 0.5) * C.dmgJitter;\n'''",
         "PRICE_READ_ANCHOR = '''    /* --- weight --- */\n'''"),
        ("the damage clause written twice", "PRICE_LINE_ANCHOR + '''self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : '''",
         "PRICE_LINE_ANCHOR + '''self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : '''"),
    ]
    print("(2) negative copies of the builder: one insert made wrong, each must refuse")
    for i, (what, a, b) in enumerate(NEG):
        assert SRC.count(a) == 1, (what, a)
        nb = d / f"neg{i}_goreshard_build.py"
        nb.write_text(SRC.replace(a, b, 1), encoding="utf-8")
        stage, src = ("1", BASE) if "PRICE_READ_ANCHOR = " in a else ("2", STUB)
        if stage == "1":
            # the read anchor moves: build the stub with the copy, then stage 2 on it
            rc0, last0, _ = run(nb, "1", BASE, d / f"sc-goreshard-neg{i}-stub.html")
            src = d / f"sc-goreshard-neg{i}-stub.html"
            stage = "2"
        out = d / f"sc-goreshard-neg{i}.html"
        rc, last, exists = run(nb, stage, src, out)
        good = rc != 0 and not exists
        ok_all &= good
        print(f"  {'REFUSES' if good else 'WROTE!!'}  {what:<60} -> {last[:120]}")
print(f"\n{'ALL REFUSE' if ok_all else 'A HOLE: some run wrote'}")
sys.exit(0 if ok_all else 1)
