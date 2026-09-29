"""THIRD REVIEW ROUND: every mutant's v5 probe run against its v4 run (the second-round probe). Outside [2] and [7] the v5
probe changed only its JSON writer, so each of [1] [3] [4] [5] [6] [8] must read the same (PASS, or FAIL with the same
count), and the header's mechanism lines the same. [2] and [7] may only gain reads. Prints one line a mutant.
    python v5_vs_v4_mut.py"""
import pathlib, re
R = pathlib.Path(__file__).parent
M = ["m1-window", "m2-clock", "m3-arrows", "m4-cd", "m5-shove", "m6-bank", "m7-stop", "m8-side",
     "r1-netsplice", "r2-pinned", "r3-castcd", "r4-noward", "r5-stun", "r6-hex", "r7-castsunder"]
def checks(t):
    out = {}
    for k, res, rest in re.findall(r"^\s*\[(\d)\] (PASS|FAIL)(.*)$", t, re.M):
        m = re.search(r"(\d+) FAIL", rest)
        out[k] = "PASS" if res == "PASS" else (m.group(1) if m else "NOT EXERCISED")
    return out
def mech(t):
    L = t.splitlines(); h = [i for i, l in enumerate(L) if l.startswith("BULWARK PROBE")]
    return L[h[0] + 1:h[0] + 4] if h else None
allok = True
for m in M:
    v4 = R / (f"probe_mut_{m}_v4.txt" if m.startswith("m") else f"probe_mut_{m}.txt")
    v5 = R / f"probe_mut_{m}_v5.txt"
    if not (v4.exists() and v5.exists() and "/8" in v5.read_text(encoding="utf-8")):
        print(f"{m:<14} MISSING ({v4.name} {v4.exists()}, {v5.name} {v5.exists()})"); allok = False; continue
    a, b = v4.read_text(encoding="utf-8"), v5.read_text(encoding="utf-8")
    ca, cb = checks(a), checks(b)
    same = [k for k in "134568" if ca.get(k) == cb.get(k)]
    diff = [f"[{k}] {ca.get(k)} -> {cb.get(k)}" for k in "134568" if ca.get(k) != cb.get(k)]
    gain = [f"[{k}] {ca.get(k)} -> {cb.get(k)}" for k in "27" if ca.get(k) != cb.get(k)]
    mm = mech(a) == mech(b)
    ok = not diff and mm
    allok &= ok
    print(f"{m:<14} {'SAME' if ok else 'DIFFERS'}   [1][3][4][5][6][8] {'identical' if not diff else ', '.join(diff)}   "
          f"mechanism lines {'identical' if mm else 'DIFFER'}   [2][7]: {', '.join(gain) if gain else 'identical'}")
print("\nEVERY MUTANT: v5 reads [1] [3] [4] [5] [6] [8] and the mechanism exactly as v4 did" if allok else "\nNOT ALL (see above)")
