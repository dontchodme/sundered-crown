# relic_rate on the stage-5 link with no --set, against the sweep's --set dmg=<blade> run on stage 3: every foe's rate,
# the by-type rates, both sides' rates and the mean duration must be identical.
import hashlib, json, pathlib, sys
R = pathlib.Path(sys.argv[1]); link, sweep_link, blade = sys.argv[2], sys.argv[3], sys.argv[4]
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
L = [f"relic_rate on {pathlib.Path(link).name} ({sha(link)}) with no --set, against --set dmg={blade} on "
     f"{pathlib.Path(sweep_link).name} (the sweep, run on round 2's stage 3, 0dac0cefbff88ead; round 3's {sha(sweep_link)} differs only in a comment)"]
ok = True
for b in (2207, 2317):
    s = json.loads((R / f"stage5_rr_d{blade}_{b}.json").read_text()); n = json.loads((R / f"stage5_rr_built_b205_{b}.json").read_text())
    foe = s["byFoe"] == n["byFoe"]; typ = s["byType"] == n["byType"]
    rates = (s["rate"], s["rateA"], s["rateB"]) == (n["rate"], n["rateA"], n["rateB"]); dur = s["dur"] == n["dur"]
    this = foe and typ and rates and dur and s["games"] == n["games"]; ok &= this
    L.append(f"seed0 {b}: --set {s['rate']:.4f} A {s['rateA']:.4f} B {s['rateB']:.4f} dur {s['dur']:.6f}  |  built, no set "
             f"{n['rate']:.4f} A {n['rateA']:.4f} B {n['rateB']:.4f} dur {n['dur']:.6f}")
    L.append(f"   every foe's rate identical: {foe} ({len(n['byFoe'])} foes); by type identical: {typ}; rates identical: {rates}; "
             f"mean duration identical: {dur}  ->  {'REPRODUCED EXACTLY' if this else 'DIFFERENT'}")
print("\n".join(L)); sys.exit(0 if ok else 1)
