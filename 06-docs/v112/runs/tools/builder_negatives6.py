"""v112 §6a: THE STAGE-6 SCAN CAN FAIL. Copies of tools/heartwood_build.py, each with ONE forbidden change to a
row of its S6 table (a line added to tickGrove, the drawing methods, the Sfx arms, the fighter's fields, a retired
row, the root's one voice line or the life row; or a row moved, doubled or added), run as stage 6 on the final
(sc-heartwood-b11); every copy must REFUSE, before writing, for the reason named. A final copy with nothing changed
must build the stage-6 link byte-identical (ceba5e801f4cf91b: the control of the control).
    python builder_negatives6.py <S>"""
import hashlib, pathlib, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = S / "tmp" / "neg6"; T.mkdir(parents=True, exist_ok=True)
PY = sys.executable
src = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_build.py").read_text(encoding="utf-8")
S6AT = src.index("\nS6 = [\n")
WANT = "ceba5e801f4cf91b"

TICK = "        f.groveAge += dt;\n"                     # inside tickGrove, the window's branch
DRAW = "  _groveBits(f){\n    const c = this.ctx;\n"      # inside the drawing methods
SFX_ = "          const g = 0.2768;\n"                   # inside the cast's Sfx arm
FLD = "    this.groveMoteAcc = 0;\n"                     # the fighter's fields
RET = "       cannot erase it. */\n"                     # the plate's retiring comment
for a in (TICK, DRAW, SFX_, FLD, RET):
    assert src.count(a) == 1 and src.index(a) > S6AT, a

def add(anchor, line, ind="        "):
    return lambda s: s.replace(anchor, anchor + ind + line + "\n", 1)

def sub(old, new):
    def f(s):
        assert s.count(old) == 1, old[:60]
        return s.replace(old, new, 1)
    return f

VOICE_OLD = " '''    T.rooted++;''',\n '''    T.rooted++;\n"
LIFE_OLD = "              oathwound: 1.5, '''),"
ARM0 = " '''        } else if (w === \"heartwood\"){"
RC = "        } else {                                        // rune-crack"
SPEC = ("    heartwood: { mode: 'fall', n: 1050, sp: [30, 120], grav: 110, drag: 1.0,\n"
        "                 life: [0.80, 1.70], heavy: 0.02, size: [0.6, 1.9],\n"
        "                 spawn: 0.85, up: 0 },\n")
END = "\n]\n\n# ------------------------------------------------------- the insert scan --"

BAD = [
    # tickGrove: the simulation, by every road
    ("tick: nudge the foe", add(TICK, "foe.vx += 1e-9;"), "writes foe.vx"),
    ("tick: free the pin", add(TICK, "foe.pin = 0;"), "writes foe.pin"),
    ("tick: free the weapon", add(TICK, "foe.pinFree = 1;"), "writes foe.pinFree"),
    ("tick: feed the charge", add(TICK, "f.charge += 0.01;"), "writes f.charge"),
    ("tick: draw the RNG", add(TICK, "const r0 = this.rng();"), "draws the RNG"),
    ("tick: Math.random", add(TICK, "const r1 = Math.random();"), "adds a Math.random"),
    ("tick: take the ultFx slot", add(TICK, "this.ultFx = null;"), "ultFx"),
    ("tick: stop the world", add(TICK, "this.hitStop = 0.05;"), "writes this.hitStop"),
    ("tick: a status", add(TICK, 'foe.apply("entangle", 1, "a");'), "calls foe.apply("),
    ("tick: hurt", add(TICK, "this.hurt(foe, 1, f);"), "calls this.hurt("),
    ("tick: a beat", add(TICK, 'this.beat({ kind: "ult" });'), "calls this.beat("),
    ("tick: a voice", add(TICK, 'SFX.play("ult", { w: "heartwood-root" });'), "calls SFX.play("),
    ("tick: a status by hand", add(TICK, "foe.status.entangle.stacks = 4;"), "writes foe.status.entangle.stacks"),
    ("tick: Object.assign", add(TICK, "Object.assign(foe, { stun: 2 });"), "uses 'Object'"),
    ("tick: write by index", add(TICK, 'foe["stun"] = 2;'), "through an index"),
    ("tick: destructure", add(TICK, "[foe.vx, foe.vy] = [0, 0];"), "through an index or a destructuring"),
    ("tick: the shared weapon", add(TICK, "f.w.reach = 200;"), "writes f.w.reach"),
    ("tick: a module table", add(TICK, "CONFIG.physics.ballR = 30;"), "reaches a module table"),
    ("tick: the tags' array", add(TICK, "this.tags.splice(0, 1);"), "calls this.tags.splice("),
    ("tick: a bare global", add(TICK, "hitStop = 1;"), "assigns `hitStop`"),
    ("tick: an alias", add(TICK, "const q0 = foe; q0.stun = 1;"), "writes q0.stun"),
    ("tick: an arrow", add(TICK, "[foe].forEach(g2 => g2);"), "has an arrow"),
    ("tick: call through a bracket", add(TICK, 'foe["takeHitstun"](5);'), "uses ']('"),
    ("tick: new", add(TICK, "const z0 = new Set();"), "uses 'new'"),
    ("tick: a bare function", add(TICK, "hurtFoe(foe, 1);"), "calls hurtFoe("),
    ("tick: the root again", add(TICK, "this.rootBlow(f);"), "calls this.rootBlow("),
    ("tick: a prefix step", add(TICK, "++foe.hits;"), "writes foe.hits"),
    ("tick: window", add(TICK, "window.x0 = 1;"), "uses 'window'"),
    ("tick: eval", add(TICK, "eval('1');"), "uses 'eval'"),
    ("tick: delete", add(TICK, "delete foe.pinV;"), "uses 'delete'"),
    ("tick: a call through .call", add(TICK, "Math.max.call(null, 1);"), "calls Math.max.call("),
    # the drawing methods: the canvas and nothing else
    ("draw: move the ball", add(DRAW, "f.x += 1;", "    "), "writes f.x"),
    ("draw: the picture's clock", add(DRAW, "f.groveFade = 0;", "    "), "writes f.groveFade"),
    ("draw: the tags", add(DRAW, "this.tags.length = 0;", "    "), "writes this.tags.length"),
    ("draw: rebind the canvas", add(DRAW, "c = f;", "    "), "reassigns `c`"),
    ("draw: a voice", add(DRAW, 'SFX.play("hit", {});', "    "), "calls SFX.play("),
    ("draw: the synth", add(DRAW, "this._tone(0, {});", "    "), "calls this._tone("),
    ("draw: a second arrow", add(DRAW, "const z1 = () => 0;", "    "), "has an arrow"),
    # the Sfx arms, the fields, a retired row, the one-line rows
    ("sfx: write the synth's state", add(SFX_, "this.on = false;", "          "), "writes this.on"),
    ("sfx: the root's voice here", add(SFX_, 'SFX.play("ult", { w: "heartwood-root" });', "          "), "calls SFX.play("),
    ("fields: a sim field", add(FLD, "this.pin = 0;", "    "), "writes this.pin"),
    ("fields: Tendril's marker", add(FLD, "this.twineHeld = 0;", "    "), "writes this.twineHeld"),
    ("retired: code in a comment row", add(RET, "const k0 = 1;", "    "), "adds code"),
    ("life: keep a life entry", sub(LIFE_OLD, "              oathwound: 1.5, heartwood: 1.4, '''),"), "not that line alone"),
    ("voice: twice", sub('    SFX.play("ult", { w: "heartwood-root" });\'\'\'),',
                         '    SFX.play("ult", { w: "heartwood-root" });\n    SFX.play("ult", { w: "heartwood-root" });\'\'\'),'),
     "not that line alone"),
    # the page: where things land
    ("page: the voice before the kill's return", sub(VOICE_OLD, " '''    T.blows++;''',\n '''    T.blows++;\n"),
     "after the killing blow's return"),
    ("page: the arms after the fallback", sub(ARM0, " '''" + RC + "\n" + ARM0[4:]), "rune-crack fallback is not kept"),
    ("page: SPECS.heartwood taken out", sub(END, "\n\n('take the field out',\n '''" + SPEC + "''',\n ''''''),\n" + END[1:]),
     "touched the inlined fx.js"),
    ("page: a second presentation call", add(FLD, "this.tickGrove(dt);", "    "), "is not added exactly once"),
]
b11 = S / "links" / "sc-heartwood-b11.html"
lines, ok = [], True
for i, (name, fn, why) in enumerate(BAD + [("CONTROL: nothing changed", None, None)]):
    b = src if fn is None else fn(src)
    assert fn is None or b != src, name
    bp = T / f"heartwood_build_neg6_{i:02d}.py"; bp.write_text(b, encoding="utf-8", newline="\n")
    out = T / f"sc-heartwood-neg6-{i:02d}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(bp), "--stage", "6", "--src", str(b11), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    txt = (r.stdout + r.stderr)
    if fn is None:
        good = r.returncode == 0 and out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()[:16] == WANT
        lines.append(f"{name:<40} rc {r.returncode}  -> " + (f"BUILDS, byte-identical to sc-heartwood-b11-fx ({WANT})" if good else "!! " + txt[-300:]))
    else:
        refused = [l for l in txt.splitlines() if "REFUSING" in l]
        good = r.returncode != 0 and not out.exists() and bool(refused) and why in refused[0]
        lines.append(f"{name:<40} rc {r.returncode}  -> " + (f"REFUSED: {refused[0].strip()[:130]}" if good
                     else "!! NOT REFUSED FOR THE REASON (" + why + "): " + txt[-300:].replace(chr(10), ' | ')))
    ok &= good
lines.append("")
lines.append(f"{len(BAD)} negative copies of the stage-6 table, every one refused for its reason; the unmodified copy "
             "builds the stage-6 link" if ok else "!! THE STAGE-6 SCAN MISSED ONE")
text = "\n".join(lines) + "\n"
(S / "runs" / "builder_negatives6.txt").write_text(text, encoding="utf-8", newline="\n"); print(text)
