"""Stage 6's probe runs against stage 5's: (1) the new probe on the b7.5 (--drawn 0) against the stages 1-5
probe's own run on it (runs/probe_b7.5.*); (2) the new probe on the fx link against the new probe on the b7.5.
Each: the printed lines (the time in the page aside) -- only the stage-6 lines may differ -- and every counter,
tally and per-fight digest of [1]-[6]."""
import json, pathlib, re, sys
R = pathlib.Path(r"<scratch>/runs")
S6 = ("  stage 6", "  [7]", "  [8]", "  drawn subset")
def lines(p):
    out = []
    for ln in (R / p).read_text(encoding="utf-8").splitlines():
        ln = re.sub(r"\s+\(\d+s in the page\)", "", ln)
        out.append(ln)
    return out
OLD6 = set()   # the counters [1]-[6] use: every name the stages 1-5 probe counted on the b7.5
def comp(a, b, title):
    print(f"\n{title}: {a} -> {b}")
    la, lb = lines(a + ".txt"), lines(b + ".txt")
    la = [l for l in la if not l.startswith(S6) and "UNMAKING PROBE" not in l]
    lb2 = [l for l in lb if not l.startswith(S6) and "UNMAKING PROBE" not in l]
    lb2 = [l for l in lb2 if not re.match(r"\s+\d+/\d+$", l)]
    la = [l for l in la if not re.match(r"\s+\d+/\d+$", l)]
    same = la == lb2
    print(f"  the printed lines, the stage-6 lines, the header (its file name) and the score aside: {'IDENTICAL' if same else 'DIFFERENT'} ({len(la)} lines)")
    if not same:
        import difflib
        for d in difflib.unified_diff(la, lb2, lineterm="", n=0): print("   ", d)
    ja, jb = json.loads((R / (a + ".json")).read_text()), json.loads((R / (b + ".json")).read_text())
    keys = sorted(ja["n"])
    moved = [k for k in keys if ja["n"].get(k) != jb["n"].get(k)]
    extra = sorted(k for k in jb["n"] if k not in ja["n"])
    print(f"  counters of the first run: {len(keys)}, all equal in the second: {not moved} {moved[:8]}")
    print(f"  counters only in the second (stage 6's): {len(extra)}")
    for k in ("T", "TS", "digest", "fights", "win", "u"):
        print(f"  {k}: {'equal' if ja[k] == jb[k] else 'DIFFERENT'}")
    return same and not moved and all(ja[k] == jb[k] for k in ("T", "TS", "digest", "fights", "win", "u"))
ok = comp("probe_b7.5", "stage6_probe_b7.5", "(1) THE NEW PROBE ON THE b7.5 AGAINST THE STAGES 1-5 PROBE'S OWN RUN")
if (R / "stage6_probe_fx.json").exists():
    ok &= comp("stage6_probe_b7.5", "stage6_probe_fx", "(2) THE NEW PROBE ON THE FX LINK AGAINST THE NEW PROBE ON THE b7.5")
print("\nPASS" if ok else "\nFAIL")
