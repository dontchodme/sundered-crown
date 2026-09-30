"""v113 §5: STAGE 6'S SCAN CAN FAIL. Copies of tools/thornwake_build.py, each with ONE forbidden line added to
one of the S6 table's rows (the picture's tickBrier, its drawing methods, a voice line on the sim path, a one-line
row, a retiring row), run as stage 6 on the stage-5 link; every copy must REFUSE, before writing, for the reason
named. A final copy with nothing added must build the fx link byte-identical (the control of the control).
    python neg_builder6.py <S> <want sha16 of the fx link>"""
import hashlib, pathlib, subprocess, sys
S = pathlib.Path(sys.argv[1]); WANT = sys.argv[2]; T = S / "tmp" / "neg6"; T.mkdir(parents=True, exist_ok=True)
PY = sys.executable
src = pathlib.Path("C:/dev/sundered-crown/tools/thornwake_build.py").read_text(encoding="utf-8")
src = src.replace('HERE = pathlib.Path(__file__).parent', 'HERE = pathlib.Path("C:/dev/sundered-crown/tools")', 1)
TICK = "      if (f.brierTagT > 0) f.brierTagT -= dt;\n"                  # inside tickBrier
DRAW = "  drawBrier(m){\n    const a = m.a, b = m.b;\n"                      # inside the drawing methods
VOICE = '    SFX.play("ult", { w: "thornwake-crackle" });' + "'" * 3        # the crackle's sim line, the row's end
ONE = "    this.drawBrierTop(m);\n"                                         # a one-line row's added line
RET = "       CAST only and nothing draws from it. */\n"                   # a retiring row (drawUltUnder's)
for an in (TICK, DRAW, VOICE, RET):
    assert src.count(an) == 1, an
assert src.count(ONE) == 1, ONE          # the row's added line, once in the table
BAD = [
    (TICK, "unpin the foe", "foe.pin = 0;", "writes the simulation"),
    (TICK, "nudge the foe", "foe.vx *= 0.99;", "writes the simulation"),
    (TICK, "clear the thorns' cooldown", "f.brambleCd = 0;", "writes the simulation"),
    (TICK, "stop the world", "this.hitStop = 0.1;", "writes the simulation"),
    (TICK, "empty the brambles", "this.brambles.length = 0;", "writes this.brambles.length"),
    (TICK, "an invisible field on the foe", "foe.lastBrier = 1;", "writes foe.lastBrier"),
    (TICK, "the other fighter's green", "this.a.brierGreen = 1;", "writes this.a.brierGreen"),
    (TICK, "draw the RNG", "const r0 = this.rng();", "draws the RNG"),
    (TICK, "Math.random", "const r1 = Math.random();", "draws the RNG"),
    (TICK, "take the ultFx slot", "this.ultFx = null;", "ultFx"),
    (TICK, "voice it from the picture", 'SFX.play("ult", { w: "thornwake-bite" });', "plays a voice outside"),
    (TICK, "hurt from the picture", "this.hurt(foe, 1, f);", "calls into the simulation"),
    (TICK, "entangle from the picture", 'foe.apply("entangle", 1, side);', "calls into the simulation"),
    (TICK, "file a beat", 'this.beat({ kind: "ult" });', "calls into the simulation"),
    (TICK, "write the shared weapon", "f.w.dmg = 13;", "shared weapon row"),
    (TICK, "write a module table", "STATUS.entangle.tip = null;", "shared module table"),
    (TICK, "delete a status", "delete foe.status.entangle;", "deletes"),
    (TICK, "write a picture record by index", "f.brierPic[0] = null;", "through an index"),
    (TICK, "clear the tags", "this.tags.length = 0;", "writes this.tags.length"),
    (TICK, "strike the synth", "this._tone(0, {});", "strikes the synth"),
    (DRAW, "end the match from a drawing", "m.over = true;", "writes the simulation"),
    (DRAW, "a tag from a drawing", "this.tags.push({});", "touches the tags outside tickBrier"),
    (DRAW, "write a field from a drawing", "a.brierGreen = 0;", "writes a.brierGreen"),
    (DRAW, "a canvas that is not the renderer's", "const c = m.a;", "binds `c`"),
    (VOICE, "a sim line that is not its voice alone", "const k = 1;", "not its voice alone"),
    (ONE, "a one-line row with a second line", "this.drawBrier(m);", "not that line alone"),
    (RET, "a retiring row that adds code", "c.fill();", "adds code"),
]
stage5 = S / "links" / "sc-thornwake-b26.5.html"
lines, ok = [], True
for i, (an, name, bad, why) in enumerate(BAD + [(None, "CONTROL: nothing added", None, None)]):
    if bad is None:
        b = src
    elif an == ONE:
        k = src.find(ONE)
        b = src[:k + len(ONE)] + "    " + bad + "\n" + src[k + len(ONE):]
    else:
        ind = an[:len(an) - len(an.lstrip())]
        if an.endswith("'" * 3):
            b = src.replace(an, an[:-3] + "\n" + ind + bad + "'" * 3, 1)
        else:
            b = src.replace(an, an + ind + bad + "\n", 1)
    bp = T / f"thornwake_build_neg6_{i:02d}.py"; bp.write_text(b, encoding="utf-8", newline="\n")
    out = T / f"sc-thornwake-neg6-{i:02d}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(bp), "--stage", "6", "--src", str(stage5), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    txt = (r.stdout + r.stderr)
    if bad is None:
        good = r.returncode == 0 and out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()[:16] == WANT
        lines.append(f"{name:<40} rc {r.returncode}  -> " + (f"BUILDS, byte-identical to sc-thornwake-b26.5-fx ({WANT})" if good else "!! " + txt[-200:]))
    else:
        refused = [l for l in txt.splitlines() if "REFUSING" in l]
        good = r.returncode != 0 and not out.exists() and bool(refused) and why in txt[txt.find("REFUSING"):]
        where = {TICK: "tickBrier", DRAW: "drawBrier", VOICE: "the crackle's line", ONE: "drawBrierTop's call", RET: "drawUltUnder's retirement"}[an]
        msg = refused[0].split(" -- ", 1)[-1].strip()[:110] if refused else ""
        lines.append(f"{name:<40} +{bad:<44} in {where:<26} rc {r.returncode}  -> "
                     + (f"REFUSED: {msg}" if good else "!! NOT REFUSED FOR THE REASON: " + txt[-240:].replace(chr(10), ' | ')))
    ok &= good
lines.append("")
lines.append(f"{len(BAD)} negative copies, every one refused for its reason and wrote nothing; the unmodified copy builds the fx link"
             if ok else "!! THE SCAN MISSED ONE")
text = "\n".join(lines) + "\n"
(S / "runs" / "stage6_builder_negatives.txt").write_text(text, encoding="utf-8", newline="\n"); print(text)
