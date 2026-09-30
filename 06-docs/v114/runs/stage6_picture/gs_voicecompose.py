"""[4c] COMPOSE WITH GORESHARD'S OWN VOICE ROWS before they are on disk: the voice lab's three anchors (copied from
tools/goreshard_voice_lab.py into scratch at this moment; the lab is being edited by the voice stage), its resolveHit
row EXACTLY (RH_CODE, mode before), and its two Sfx rows with stand-in code (mode before, as the lab writes them;
their code sits inside Sfx.play, nowhere near these rows). Both orders on the base and on the batch tip carries.
SCRATCH."""
import sys, json, pathlib, hashlib
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "vcopy")); sys.path.insert(0, "C:/dev/sundered-crown/tools")
import gs_rows as P
import gvl
R = json.loads((HERE / "rows_final.json").read_bytes().decode("utf-8"))
V = [dict(label="voice: resolveHit's priced call", anchor=gvl.RH_ANCHOR, mode="before", code=gvl.RH_CODE),
     dict(label="voice: Sfx hit branch (stand-in)", anchor=gvl.HIT_ANCHOR, mode="before", code="      /* stand-in for the voice's hit branch */\n"),
     dict(label="voice: Sfx cast arm (stand-in)", anchor=gvl.SFX_ANCHOR, mode="before", code="        /* stand-in for the voice's cast arm */\n")]
def apply(s, rows):
    for r in rows:
        n = s.count(r["anchor"]); assert n == 1, (r["label"], n)
        s = P.one(s, r["anchor"], r["code"], r["mode"], r["label"])
    return s
tips = [("base b10.25", P.SRC)] + [(d.name, d / "sc-goreshard-b10.25.html") for d in sorted((HERE / "carry").iterdir()) if (d / "sc-goreshard-b10.25.html").exists() and "+" not in d.name]
for name, p in tips:
    s = p.read_bytes().decode("utf-8")
    for r in R + V:
        for q in R + V:
            if r is not q: assert q["anchor"] not in r["code"], (r["label"], q["label"])
    x = apply(apply(s, V), R); y = apply(apply(s, R), V)
    P.syntax_check(x)
    # the float line and the voice's line are distinct lines in resolveHit, the float's first
    i, j = x.index("(1 + 0.1 * priceN);"), x.index(gvl.RH_ANCHOR)
    print(f"[4c] {name}: voice-then-picture == picture-then-voice {x == y}; parses; every anchor once; "
          f"the float line precedes the voice's call by {x[i:j].count(chr(10))} lines")
print("RH_ANCHOR:", gvl.RH_ANCHOR.strip())
