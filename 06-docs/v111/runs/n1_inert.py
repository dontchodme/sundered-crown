"""v111's review, note 1 (no second hex on the killing blow, the lab's guard) and note 2 (the insert
moved above Deadfall's comment): do they move any fight? relic_rate on the FIXED links (no --set)
against the stage-5 grid, which ran on the PRE-REVIEW stage-3 link (29c3ea7b9e3e5f91, --set dmg), both
blocks, every field relic_rate reports. Identical => the grid, the table and the ladder stand.
    python n1_inert.py <runs dir>"""
import json, sys
S = sys.argv[1]
ok = True
for tag, blade in (("unm8.81", "8.81"), ("b8.3", "8.3"), ("b7.7", "7.7"), ("b7.5", "7.5")):
    for B in ("2207", "2317"):
        a = json.load(open(f"{S}/stage5_rr_d{blade}_{B}.json")); b = json.load(open(f"{S}/stage5_rr_link_{tag}_{B}.json"))
        d = [k for k in ("rate", "rateA", "rateB", "games", "dur", "timeouts", "byType", "byFoe") if a[k] != b[k]]
        ok &= not d
        print(f"blade {blade:>4} block {B}: pre-review stage-3 link {100*a['rate']:.2f}% mean {a['dur']:.6f}s | fixed link "
              f"sc-spellbreaker-{'unmaking' if tag == 'unm8.81' else tag} {100*b['rate']:.2f}% mean {b['dur']:.6f}s | "
              f"{a['games']} fights, 37 foes: " + ("IDENTICAL" if not d else f"DIFFER in {d}"))
print("THE FIX MOVES NO FIGHT: the stage-5 grid stands" if ok else "THE FIX MOVES FIGHTS: re-run the grid")
sys.exit(0 if ok else 1)
