"""Stage 6's builder checks, on the builder as it stands (tools/censer_build.py):
  A. all five links rebuild byte-identical from the bare tip (sc-tendril-t3), LF, no CR;
  B. the refusals: stage 6 twice, on stages 3 / 2 / 1 and the bare tip, over an existing link, to a
     name not sc-censer*; stage 5 on the fx link;
  C. negative guards: a scratch copy of the builder with ONE forbidden thing written into a stage-6
     insert must refuse; the unmutated copy must write the fx link (3d68c7648a9cb3a8).
Exit 1 on any FAIL."""
import hashlib, pathlib, shutil, subprocess, sys

S = pathlib.Path(__file__).resolve().parent.parent
REPO = pathlib.Path("C:/dev/sundered-crown")
B = REPO / "tools" / "censer_build.py"
T = S / "s6" / "checks6"
if T.exists():
    shutil.rmtree(T)
T.mkdir()
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
LINKS = {"sc-censer-stub": "56626e03654f3daf", "sc-censer-ground": "9da88c11cb87a3a2",
         "sc-censer-consecration": "2ce681c11f5d4183", "sc-censer-consecration-b25.5": "56c49ad3f0ccb3aa",
         "sc-censer-consecration-b25.5-fx": "3d68c7648a9cb3a8"}
fails = 0


def run(builder, stage, src, out):
    r = subprocess.run([sys.executable, str(builder), "--stage", stage, "--src", str(src), "--out", str(out)],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def say(ok, msg):
    global fails
    fails += 0 if ok else 1
    print(("  ok    " if ok else "  FAIL  ") + msg)


print(f"builder {B.name} {sha(B)}")
print("A. the five links from the bare tip")
src = REPO / "02-chain" / "sc-tendril-t3.html"
for st, name in zip("12356", LINKS):
    out = T / f"{name}.html"
    rc, log = run(B, st, src, out)
    ok = rc == 0 and out.exists() and sha(out) == LINKS[name] and b"\r" not in out.read_bytes()
    say(ok, f"stage {st} -> {name}.html {sha(out) if out.exists() else '-'} (want {LINKS[name]}; LF)")
    if not ok:
        print(log[-800:])
    src = out
    same = out.read_bytes() == (S / "links" / f"{name}.html").read_bytes()
    say(same, f"   == links/{name}.html byte for byte")

print("B. the refusals")
L = {k: S / "links" / f"{k}.html" for k in LINKS}
cases = [
    ("stage 6 twice (on the fx link)", "6", L["sc-censer-consecration-b25.5-fx"], T / "sc-censer-x1.html"),
    ("stage 6 on stage 3 (28.77)", "6", L["sc-censer-consecration"], T / "sc-censer-x2.html"),
    ("stage 6 on stage 2", "6", L["sc-censer-ground"], T / "sc-censer-x3.html"),
    ("stage 6 on stage 1", "6", L["sc-censer-stub"], T / "sc-censer-x4.html"),
    ("stage 6 on the bare tip", "6", REPO / "02-chain" / "sc-tendril-t3.html", T / "sc-censer-x5.html"),
    ("stage 6 over an existing link", "6", L["sc-censer-consecration-b25.5"], T / "sc-censer-consecration-b25.5-fx.html"),
    ("stage 6 to a name not sc-censer*", "6", L["sc-censer-consecration-b25.5"], T / "sc-other-fx.html"),
    ("stage 5 on the fx link", "5", L["sc-censer-consecration-b25.5-fx"], T / "sc-censer-x6.html"),
]
for what, st, s_, o_ in cases:
    pre = o_.exists()
    before = o_.read_bytes() if pre else None
    rc, log = run(B, st, s_, o_)
    untouched = (o_.read_bytes() == before) if pre else not o_.exists()
    last = [ln for ln in log.strip().splitlines() if ln.strip()][-1] if log.strip() else ""
    say(rc != 0 and untouched, f"{what}: refused, nothing written -- {last.strip()[:110]}")

print("C. negative guards on a scratch copy (one forbidden thing in a stage-6 insert each)")
TICK = "      if (dK > 0) f.consPulse = 1;\n"
DRAW = "    const c = this.ctx, n = m.inset || 0;\n"
HEAD = "    const c = this.ctx, R = CONFIG.physics.ballR;\n"
BELL = '        SFX.play("ult", { w: "censer-disc", n: n_ }); }'
HEAL = '          SFX.play("spark", { collect: true, n: f.stacks("blessing") });'
FLD = "    this.consTagB = false;\n"
SFXA = "          const n = clamp(Math.round(p.n || 0), 1, 5), g = 0.04177, D = 0.612;\n"
MUT = [
    ("a sim write in tickConsecration (the foe nudged)", TICK, TICK + "      foe.vx += 1e-9;\n"),
    ("the RNG in a draw method", DRAW, DRAW + "    const q_ = m.rng();\n"),
    ("the one ultFx slot in tickConsecration", TICK, TICK + "      const u_ = this.ultFx;\n"),
    ("a beat in tickConsecration", TICK, TICK + '      if (dK > 0) this.beat("smite", foe);\n'),
    ("a hurt in the heal row", HEAL, HEAL + "\n          foe.hurt(1, f);"),
    ("a status laid (stun) in tickConsecration", TICK, TICK + '      if (dK > 0) foe.apply("stun", 1, side);\n'),
    ("a splice of the sim's discs", TICK, TICK + "      if (dK > 99) G.splice(0, 1);\n"),
    ("an index write into the sim's discs", TICK, TICK + "      if (dK > 99) G[0] = null;\n"),
    ("a write to the tally", TICK, TICK + "      if (dK > 99) T.ticks = 0;\n"),
    ("Math.random in a draw method", DRAW, DRAW + "    const q_ = Math.random();\n"),
    ("a shared table through an alias", TICK, TICK + "      const Q_ = STATUS.smite; if (dK > 99) Q_.dur = 1;\n"),
    ("the shared weapon (w.reach)", HEAD, HEAD + "    if (a.consFade > 9) a.w.reach = 1;\n"),
    ("a sim write in a draw method (the match's clock)", DRAW, DRAW + "    if (m.t < 0) m.t = 0;\n"),
    ("the disc bell's line changed (n + 1)", BELL, BELL.replace("n: n_ }", "n: n_ + 1 }")),
    ("a voice in the picture's fields row", FLD, FLD + '    SFX.play("ult", { w: "censer" });\n'),
    ("a sim write in the fighter-fields row", FLD, FLD + "    this.charge = 0;\n"),
    ("the synth struck outside the Sfx row", TICK, TICK + "      if (dK > 99) SFX._tone(0, {});\n"),
    ("a clean edit in the Sfx arm (a local; must still WRITE its page, a different one)", SFXA,
     SFXA + "          const unused_ = 1;\n"),
]
src = S / "links" / "sc-censer-consecration-b25.5.html"
btxt = B.read_text(encoding="utf-8")
for i, (what, old, new) in enumerate(MUT):
    n = btxt.count(old)
    if n != 1:
        say(False, f"{what}: its hook is in the builder {n}x, not once")
        continue
    d = T / f"neg{i:02d}"
    d.mkdir()
    bp = d / "censer_build.py"
    bp.write_text(btxt.replace(old, new, 1), encoding="utf-8", newline="\n")
    out = d / "sc-censer-neg-fx.html"
    rc, log = run(bp, "6", src, out)
    last = [ln for ln in log.strip().splitlines() if ln.strip()][-1] if log.strip() else ""
    if what.startswith("a clean edit"):
        say(rc == 0 and out.exists() and sha(out) != LINKS["sc-censer-consecration-b25.5-fx"],
            f"{what}: rc {rc}, {sha(out) if out.exists() else '-'}")
    else:
        say(rc != 0 and not out.exists(), f"{what}: REFUSED -- {last.strip()[:120]}")
d = T / "clean"
d.mkdir()
bp = d / "censer_build.py"
bp.write_text(btxt, encoding="utf-8", newline="\n")
out = d / "sc-censer-clean-fx.html"
rc, log = run(bp, "6", src, out)
say(rc == 0 and out.exists() and sha(out) == LINKS["sc-censer-consecration-b25.5-fx"],
    f"the unmutated copy writes {sha(out) if out.exists() else '-'} (the fx link 3d68c7648a9cb3a8)")
print(f"\n{'0 FAIL' if not fails else f'{fails} FAIL'}")
sys.exit(1 if fails else 0)
