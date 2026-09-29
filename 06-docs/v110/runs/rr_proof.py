"""relic_rate on a written stage-5 link with no --set must reproduce the --set run on the stage-3
link exactly: the rate, both sides, the games, the mean duration, the timeouts, every type and
every foe."""
import json, sys
S, link, blade = sys.argv[1], sys.argv[2], sys.argv[3]
ok = True
for B in ("2207", "2317"):
    a = json.load(open(f"{S}/stage5_rr_d{blade}_{B}.json")); b = json.load(open(f"{S}/stage5_rr_link_{link}_{B}.json"))
    diff = [k for k in ("rate", "rateA", "rateB", "games", "dur", "timeouts", "byType", "byFoe") if a[k] != b[k]]
    ok &= not diff
    print(f"block {B}: sc-aureole-bless --set dmg={blade}: {100*a['rate']:.2f}% (A {100*a['rateA']:.2f} / B {100*a['rateB']:.2f}), "
          f"mean {a['dur']:.6f}s | sc-aureole-{link} no --set: {100*b['rate']:.2f}% (A {100*b['rateA']:.2f} / B {100*b['rateB']:.2f}), "
          f"mean {b['dur']:.6f}s | {len(a['byFoe'])} foes, every foe, type, side and the duration "
          + ("IDENTICAL" if not diff else f"DIFFER in {diff}"))
print("THE LINK IS THE MEASURED RELIC" if ok else "THE LINK IS NOT THE MEASURED RELIC")
