"""v114 scratch: the stage-6 link's [1]-[10] against the stage-5 link's, from the same probe (the picture and the
voice move no fight): every counter of [1]-[10] (the json's `n`, stage 6's own v11*/g12*/f12*/draw* keys aside),
the tally, the log, the win rate and the blow counts, equal; and the printed [1]-[10] lines equal but the header.
    python probe_cmp6.py <b10.25 json> <fx json> <b10.25 txt> <fx txt>"""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
S6 = ("v11", "g12", "f12", "draw", "x11", "x12")
na = {k: v for k, v in a["n"].items() if not k.startswith(S6)}
nb = {k: v for k, v in b["n"].items() if not k.startswith(S6)}
ok = True
for k in sorted(set(na) | set(nb)):
    if na.get(k) != nb.get(k):
        ok = False; print(f"  DIFF counter {k}: {na.get(k)} -> {nb.get(k)}")
for k in ("T", "log", "fights", "win", "blowsIn", "blowsOut", "nClock", "nCharge", "u", "blade"):
    if a[k] != b[k]:
        ok = False; print(f"  DIFF {k}: {a[k]} -> {b[k]}")
print(f"counters of [1]-[10]: {len(na)} on the b10.25, {len(nb)} on the fx link; tally {b['T']}; win {b['win']:.4f}; "
      f"log {b['log']}")
S6L = ("STAGE 6", "stage 6:", "[11]", "[12]", "floats:", "drawn subset")
la = [l for l in open(sys.argv[3], encoding="cp1252").read().splitlines()[2:] if l.strip() and not l.strip().startswith(S6L) and not l.strip().endswith(("/10", "/12"))]
lb = [l for l in open(sys.argv[4], encoding="cp1252").read().splitlines()[2:] if l.strip() and not l.strip().startswith(S6L) and not l.strip().endswith(("/10", "/12"))]
if la != lb:
    ok = False
    for x, y in zip(la, lb):
        if x != y: print(f"  DIFF line\n    {x}\n    {y}")
print(f"printed [1]-[10] lines (the header aside): {len(la)} on the b10.25, {len(lb)} on the fx link, identical: {la == lb}")
print("PASS: the stage-6 link's [1]-[10] are the stage-5 link's, number for number" if ok else "FAIL")
sys.exit(0 if ok else 1)
