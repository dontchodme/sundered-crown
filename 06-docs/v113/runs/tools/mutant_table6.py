"""Stage 6's mutant table: each mutant's probe run (the first seed, both sides, every foe, 74 fights) against the
clean fx link's on the same fights -- which checks fail and how often, and whether the fights moved (the run's
tallies, all 19 of them, and the win rate, against the clean run's).
    python mutant_table6.py <runs dir>"""
import json, pathlib, sys, hashlib
R = pathlib.Path(sys.argv[1]); M = R.parent / "mut6"
clean = json.loads((R / "stage6_probe_fx_s1.json").read_text(encoding="utf-8"))
HOW = {"mV1-closevoice": "a crackle at EVERY window close, a death's too",
       "mP1-picwrite": "the snare's picture lengthens the pin 0.05 s",
       "mP2-invisible": "tickBrier stamps `lastBrier` on the fighter"}
def fails(d):
    return {k[1:]: v for k, v in sorted(d["n"].items(), key=lambda kv: int(kv[0][1:]) if kv[0][1:].isdigit() else 99)
            if k.startswith("x") and k[1:].isdigit()}
def wr(d): return 100 * d["S"]["wins"] / max(1, d["S"]["decided"])
print(f"{'mutant':<16} {'sha16':<17} {'probe':<6} {'fails (count)':<28} {'tallies vs clean':<18} {'win':>5}  how")
print(f"{'clean fx link':<16} {'d306822d6914c08c':<17} {'10/10':<6} {'-':<28} {'-':<18} {wr(clean):5.1f}")
for m in HOW:
    d = json.loads((R / f"stage6_probe_mut_{m}.json").read_text(encoding="utf-8"))
    txt = (R / f"stage6_probe_mut_{m}.txt").read_text(encoding="utf-8")
    score = [l.strip() for l in txt.splitlines() if l.strip().endswith("/10") or l.strip().endswith("/8")][-1]
    f = fails(d)
    sha = hashlib.sha256((M / f"{m}.html").read_bytes()).hexdigest()[:16]
    same = "EQUAL" if d["S"] == clean["S"] else "DIFFER"
    print(f"{m:<16} {sha:<17} {score:<6} {' '.join(f'[{k}] {v}x' for k, v in f.items()):<28} {same:<18} {wr(d):5.1f}  {HOW[m]}")
    for k in f:
        print(f"{'':<17}[{k}] e.g. {d['bad'].get(k, [''])[0][:150]}")
