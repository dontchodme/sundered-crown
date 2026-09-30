"""v111 §3's mutant table: each mutant's probe json against the link it was made from, fight by fight
(the probe's digest: won / lost and the length in steps), and which checks each one failed, and how
(by a VIOLATION, or as NOT EXERCISED -- its event never happened, or the stun gate's 200-run floor).
    python mutant_table.py <link probe json> <link probe txt> <mutant tag>=<json>,<txt> ...
A mutant (m*, r*) is a control only if it CHANGES FIGHTS and fails ITS OWN check and no other.
The review's own controls (q2-*, made on the stage-2 link) are judged CAUGHT if they change fights and
fail their own check by violations; any other check they fail is printed beside them."""
import json, re, sys
fin = json.load(open(sys.argv[1]))
own = {"m1-frozen": 1, "m2-stunlen": 2, "m3-global": 3, "m4-hexout": 4, "m5-drag": 5, "m6-boltkept": 6,
       "r1-hexonce": 4, "r2-hexclock": 5, "r3-shrink": 5, "r4-shrinkhit": 5, "r5-cadence": 2,
       "r2-hexclock-0.5": 5, "q2-hexclock": 5, "q2-shrink": 5}
def fails(txt):
    t = open(txt, encoding="utf-8").read()
    out = []
    for k, rest in re.findall(r"\[(\d)\] FAIL([^\n]*)", t):
        out.append((int(k), "NOT EXERCISED" in rest))
    return out
def score(txt):
    m = re.search(r"\n  (\d+)/(\d+)\s", open(txt, encoding="utf-8").read())
    return f"{m.group(1)}/{m.group(2)}" if m else "?"
print(f"link: {score(sys.argv[2])}, win {100*fin['win']:.1f}%, {fin['fights']} fights, failing {[k for k, _ in fails(sys.argv[2])] or 'none'}")
ok_all = True
for arg in sys.argv[3:]:
    tag, rest = arg.split("=", 1); js, txt = rest.split(",")
    mj = json.load(open(js))
    d0, d1 = fin["digest"], mj["digest"]
    assert [x[:3] for x in d0] == [x[:3] for x in d1], "the fights are not the same list"
    diff = sum(1 for a, b in zip(d0, d1) if a[3:] != b[3:])
    fl = fails(txt)
    viol = [k for k, ne in fl if not ne]; notex = [k for k, ne in fl if ne]
    if tag.startswith("q2-") or tag == "r2-hexclock-0.5":
        good = diff > 0 and own[tag] in viol
        verdict = "CAUGHT by its own check" + (f" (and {sorted(set(k for k, _ in fl) - {own[tag]})} too)" if len(fl) > 1 else "") if good else "NOT CAUGHT"
    else:
        good = diff > 0 and viol == [own[tag]] and not notex
        verdict = "A CONTROL" if good else "NOT A CONTROL"
        ok_all &= good
    fcount = {k: v for k, v in mj["n"].items() if re.fullmatch(r"x\d", k)}
    print(f"  {tag:<16} {score(txt):>4}  fails by violation {viol} (own [{own[tag]}]), not exercised {notex}  fail counts {fcount}   "
          f"win {100*mj['win']:.1f}%   fights changed {diff}/{len(d0)}   -> {verdict}")
print("EVERY m/r MUTANT CHANGES FIGHTS AND FAILS ITS OWN CHECK ALONE" if ok_all else "AN m/r MUTANT IS NOT A CONTROL")
sys.exit(0 if ok_all else 1)
