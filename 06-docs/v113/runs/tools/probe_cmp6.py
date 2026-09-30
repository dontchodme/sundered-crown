"""[1]-[8] of the stage-6 probe read the same fights the same way on the fx link as on the b26.5, and the new
probe reads the b26.5 exactly as the stage-5 probe did: every counter of [1]-[8], the tallies, the row and the
clock window equal. Stage 6's own counters ([9], [10], the drawn subset) are listed apart.
    python probe_cmp6.py <runs dir>"""
import json, pathlib, sys
R = pathlib.Path(sys.argv[1])
S6 = ("v_", "castVoiceOk", "crackleOk", "tickVoiceOk", "clockCloseSilent", "deathCloseSilent", "killBiteVoiced",
      "snareThenBite", "verdictQuiet", "brier", "tag", "taught", "green", "picMirrorOk", "heldOn", "heldCalls",
      "endGoneOk", "picFreshOk", "draw", "x9", "x10")
def load(n): return json.loads((R / n).read_text(encoding="utf-8"))
def split(d):
    a = {k: v for k, v in d["n"].items() if not k.startswith(S6)}
    b = {k: v for k, v in d["n"].items() if k.startswith(S6)}
    return a, b
old, base, fx = load("probe_final.json"), load("stage6_probe_b26.5.json"), load("stage6_probe_fx.json")
ok = True
for lab, A, B in (("the stage-5 probe on the b26.5  vs  the stage-6 probe on the b26.5", old, base),
                  ("the stage-6 probe on the b26.5  vs  the stage-6 probe on the fx link", base, fx)):
    a1, a6 = split(A); b1, b6 = split(B)
    same_n = a1 == b1
    same_S = A["S"] == B["S"]
    same_u = A["u"] == B["u"] and A["wantCalls"] == B["wantCalls"]
    diff = sorted(k for k in set(a1) | set(b1) if a1.get(k) != b1.get(k))
    print(f"{lab}:")
    print(f"  [1]-[8] counters: {len(a1)} vs {len(b1)} -- {'ALL EQUAL' if same_n else 'DIFFER: ' + ', '.join(diff[:12])}")
    print(f"  the tallies S ({len(A['S'])} keys): {'EQUAL' if same_S else 'DIFFER'};  the row and the clock window: {'EQUAL' if same_u else 'DIFFER'}")
    print(f"  stage 6's own counters: {len(a6)} vs {len(b6)}")
    ok &= same_n and same_S and same_u
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
