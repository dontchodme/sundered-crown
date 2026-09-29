"""Stage 6's builder checks, on the builder as it stands (tools/aureole_build.py):
  A. all six links rebuild byte-identical from the bare tip (sc-tendril-t3), LF, no CR;
  B. the refusals: stage 6 twice, on Rick's 50% link, on stages 3 / 2 / 1 and the bare tip, over an
     existing link, to a name not sc-aureole*; stage 5 on the fx link; --alt50 with stage 6;
  C. negative guards: a scratch copy of the builder with ONE forbidden thing written into a stage-6
     insert must refuse; a clean edit must still write (a different page); the unmutated copy must
     write the fx link (f3228d8d1509edbb).
Exit 1 on any FAIL."""
import hashlib, pathlib, shutil, subprocess, sys

S = pathlib.Path(__file__).resolve().parent.parent
REPO = pathlib.Path("C:/dev/sundered-crown")
B = REPO / "tools" / "aureole_build.py"
T = S / "s6" / "checks6"
if T.exists():
    shutil.rmtree(T)
T.mkdir()
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
FX = "f3228d8d1509edbb"
LINKS = [("1", "sc-aureole-stub", "21dc5fe5783980d1", None), ("2", "sc-aureole-halo", "51cd039d45f40521", None),
         ("3", "sc-aureole-bless", "bdd954b260479136", None), ("5", "sc-aureole-b12.5", "21ea91d0f3c14274", None),
         ("5", "sc-aureole-b11.5", "5a3f9c431d30bd7e", "--alt50"), ("6", "sc-aureole-b12.5-fx", FX, None)]
SRC_OF = {"sc-aureole-stub": "tip", "sc-aureole-halo": "sc-aureole-stub", "sc-aureole-bless": "sc-aureole-halo",
          "sc-aureole-b12.5": "sc-aureole-bless", "sc-aureole-b11.5": "sc-aureole-bless",
          "sc-aureole-b12.5-fx": "sc-aureole-b12.5"}
TIP = REPO / "02-chain" / "sc-tendril-t3.html"
fails = 0


def run(builder, stage, src, out, *extra):
    r = subprocess.run([sys.executable, str(builder), "--stage", stage, "--src", str(src), "--out", str(out), *extra],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def say(ok, msg):
    global fails
    fails += 0 if ok else 1
    print(("  ok    " if ok else "  FAIL  ") + msg)


print(f"builder {B.name} {sha(B)}; tip {TIP.name} {sha(TIP)}")
print("A. the six links from the bare tip")
for st, name, want, extra in LINKS:
    src = TIP if SRC_OF[name] == "tip" else T / f"{SRC_OF[name]}.html"
    out = T / f"{name}.html"
    rc, log = run(B, st, src, out, *([extra] if extra else []))
    ok = rc == 0 and out.exists() and sha(out) == want and b"\r" not in out.read_bytes()
    say(ok, f"stage {st}{' ' + extra if extra else ''} -> {name}.html {sha(out) if out.exists() else '-'} (want {want}; LF)")
    if not ok:
        print(log[-800:])
    same = out.exists() and out.read_bytes() == (S / "links" / f"{name}.html").read_bytes()
    say(same, f"   == links/{name}.html byte for byte")

print("B. the refusals")
L = {n: S / "links" / f"{n}.html" for _s, n, _w, _e in LINKS}
cases = [
    ("stage 6 twice (on the fx link)", "6", L["sc-aureole-b12.5-fx"], T / "sc-aureole-x1.html", []),
    ("stage 6 on Rick's 50% link (b11.5)", "6", L["sc-aureole-b11.5"], T / "sc-aureole-x2.html", []),
    ("stage 6 on stage 3 (16.01)", "6", L["sc-aureole-bless"], T / "sc-aureole-x3.html", []),
    ("stage 6 on stage 2", "6", L["sc-aureole-halo"], T / "sc-aureole-x4.html", []),
    ("stage 6 on stage 1", "6", L["sc-aureole-stub"], T / "sc-aureole-x5.html", []),
    ("stage 6 on the bare tip", "6", TIP, T / "sc-aureole-x6.html", []),
    ("stage 6 over an existing link", "6", L["sc-aureole-b12.5"], T / "sc-aureole-b12.5-fx.html", []),
    ("stage 6 to a name not sc-aureole*", "6", L["sc-aureole-b12.5"], T / "sc-other-fx.html", []),
    ("stage 5 on the fx link", "5", L["sc-aureole-b12.5-fx"], T / "sc-aureole-x7.html", []),
    ("--alt50 with stage 6", "6", L["sc-aureole-b12.5"], T / "sc-aureole-x8.html", ["--alt50"]),
]
for what, st, s_, o_, extra in cases:
    pre = o_.exists()
    before = o_.read_bytes() if pre else None
    rc, log = run(B, st, s_, o_, *extra)
    untouched = (o_.read_bytes() == before) if pre else not o_.exists()
    last = [ln for ln in log.strip().splitlines() if ln.strip()][-1] if log.strip() else ""
    say(rc != 0 and untouched, f"{what}: refused, nothing written -- {last.strip()[:110]}")

print("C. negative guards on a scratch copy (one forbidden thing in a stage-6 insert each)")
TICK = "        f.beneAge += dt;\n"
DRAW = "    const c = this.ctx, n = m.inset || 0;\n"
ENTRY = "      Z.voiceIn = voiceIn ? 1 : 0;\n"
HEAL = '        SFX.play("spark", { collect: true, n: f.stacks("blessing") });'
CLOSE = '      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });\n'
FLD = "    this.beneTagB = false;\n"
SFXA = "          const g = 0.04991, f = 1046.502, D = 0.314;\n"
RIM = "    const R = CONFIG.physics.ballR, x = foe.x, y = foe.y;\n"
MUT = [
    ("a sim write in tickBenediction (the foe nudged)", TICK, TICK + "        foe.vx += 1e-9;\n"),
    ("the RNG in a draw method", DRAW, DRAW + "    const q_ = m.rng();\n"),
    ("the one ultFx slot in tickBenediction", TICK, TICK + "        const u_ = this.ultFx;\n"),
    ("a beat in tickBenediction", TICK, TICK + '        if (f.beneAge > 99) this.beat({ kind: "x" });\n'),
    ("a hurt in the heal row", HEAL, HEAL + "\n        foe.hurt(1, f);"),
    ("a status laid (stun) in tickBenediction", TICK, TICK + '        if (f.beneAge > 99) foe.apply("stun", 1, "a");\n'),
    ("a splice of the sim's shots", TICK, TICK + "        if (f.beneAge > 99) this.shots.splice(0, 1);\n"),
    ("an index write into the sim's shots", TICK, TICK + "        if (f.beneAge > 99) this.shots[0] = null;\n"),
    ("a write to the tally", TICK, TICK + "        if (f.beneAge > 99) f.haloTally.smite = 0;\n"),
    ("a write to the window (its clock)", TICK, TICK + "        if (f.ultHalo && f.beneAge > 99) f.ultHalo.t = 0;\n"),
    ("voiceIn written outside the entry row", TICK, TICK + "        if (f.ultHalo) f.ultHalo.voiceIn = 0;\n"),
    ("Math.random in a draw method", DRAW, DRAW + "    const q_ = Math.random();\n"),
    ("a shared table through an alias", TICK, TICK + "        const Q_ = STATUS.smite; if (f.beneAge > 99) Q_.dur = 1;\n"),
    ("the shared weapon (w.reach)", RIM, RIM + "    if (L > 9) f.w.reach = 1;\n"),
    ("a sim write in a draw method (the match's clock)", DRAW, DRAW + "    if (m.t < 0) m.t = 0;\n"),
    ("the close voice on every close (a death included)", CLOSE,
     CLOSE.replace("Z.t >= Z.dur && f.alive && foe.alive", "Z.t >= Z.dur || !f.alive || !foe.alive")),
    ("the entry's memory changed (every inside tick an entry)", ENTRY, ENTRY.replace("voiceIn ? 1 : 0", "0")),
    ("a voice in the picture's fields row", FLD, FLD + '    SFX.play("ult", { w: "aureole" });\n'),
    ("a sim write in the fighter-fields row", FLD, FLD + "    this.charge = 0;\n"),
    ("the synth struck outside the Sfx row", TICK, TICK + "        if (f.beneAge > 99) SFX._tone(0, {});\n"),
    ("a clean edit in the Sfx arm (a local; must still WRITE its page, a different one)", SFXA,
     SFXA + "          const unused_ = 1;\n"),
]
src = S / "links" / "sc-aureole-b12.5.html"
btxt = B.read_text(encoding="utf-8")
for i, (what, old, new) in enumerate(MUT):
    n = btxt.count(old)
    if n != 1:
        say(False, f"{what}: its hook is in the builder {n}x, not once")
        continue
    d = T / f"neg{i:02d}"
    d.mkdir()
    bp = d / "aureole_build.py"
    bp.write_text(btxt.replace(old, new, 1), encoding="utf-8", newline="\n")
    out = d / "sc-aureole-neg-fx.html"
    rc, log = run(bp, "6", src, out)
    last = [ln for ln in log.strip().splitlines() if ln.strip()][-1] if log.strip() else ""
    if what.startswith("a clean edit"):
        say(rc == 0 and out.exists() and sha(out) != FX, f"{what}: rc {rc}, {sha(out) if out.exists() else '-'}")
    else:
        say(rc != 0 and not out.exists(), f"{what}: REFUSED -- {last.strip()[:120]}")
d = T / "clean"
d.mkdir()
bp = d / "aureole_build.py"
bp.write_text(btxt, encoding="utf-8", newline="\n")
out = d / "sc-aureole-clean-fx.html"
rc, log = run(bp, "6", src, out)
say(rc == 0 and out.exists() and sha(out) == FX, f"the unmutated copy writes {sha(out) if out.exists() else '-'} (the fx link {FX})")
print(f"\n{'0 FAIL' if not fails else f'{fails} FAIL'}")
sys.exit(1 if fails else 0)
