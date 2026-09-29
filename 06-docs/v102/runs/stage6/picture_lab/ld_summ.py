"""Summarise ld_measure's json: bloom share, discs, controls, legibility by component (in / out of a stop)."""
import sys, json, statistics as S
d = json.load(open(sys.argv[1]))
fr = [(x["foe"], x["seed"], x["side"], k, v) for x in d for k, v in x["got"].items()]
print(f"{len(fr)} frames, {len(d)} fights; missing: " + "; ".join(f"{x['foe']} {x['seed']}{x['side']} {x['missing']}" for x in d if x["missing"]))
med = lambda a: S.median(a) if a else float("nan")
dl = [v["arena"]["dLift"] for *_, v in fr]
pic = [v["arena"]["picOn"] for *_, v in fr]
worst = max(fr, key=lambda z: z[4]["arena"]["dLift"])
print(f"BLOOM: the picture's share of the chain's arena lift max {max(dl):+.4f} min {min(dl):+.4f} (gate +0.02) "
      f"[worst {worst[0]} {worst[1]}{worst[2]} {worst[3]}]; raw luma added max {max(pic):+.4f}; "
      f"arena clip with max {max(v['arena']['clipW'] for *_, v in fr):.4f} without {max(v['arena']['clipO'] for *_, v in fr):.4f}")
for c in ("ctrl1", "ctrl2", "ctrl3"):
    cd = [v[c]["dLift"] for *_, v in fr]
    fails = sum(1 for a in cd if a > 0.02)
    fw = [v for *_, v in fr if v["fade"] > 0 and not v["over"]]
    me90 = sum(1 for v in fw if v[c]["me"]["mean"] > 0.90 and v["disc"]["me"]["O"]["mean"] <= 0.90)
    fo90 = sum(1 for *_, v in fr if v[c]["foe"]["mean"] > 0.90 and v["disc"]["foe"]["O"]["mean"] <= 0.90)
    print(f"  CONTROL {c}: dLift max {max(cd):+.4f}, > 0.02 on {fails}/{len(fr)}; caster disc pushed past 0.90 on {me90}/{len(fw)} window frames; "
          f"foe disc pushed past 0.90 on {fo90}/{len(fr)} (max caster {max(v[c]['me']['mean'] for *_, v in fr):.3f}, foe {max(v[c]['foe']['mean'] for *_, v in fr):.3f})")
for who in ("me", "foe"):
    dd = [abs(v["disc"][who]["W"]["mean"] - v["disc"][who]["O"]["mean"]) for *_, v in fr]
    w90 = sum(1 for *_, v in fr if v["disc"][who]["W"]["mean"] > 0.90); o90 = sum(1 for *_, v in fr if v["disc"][who]["O"]["mean"] > 0.90)
    art = [v["artDisc"][who] for *_, v in fr]
    rng = (min(v["disc"][who]["W"]["mean"] for *_, v in fr), max(v["disc"][who]["W"]["mean"] for *_, v in fr))
    print(f"DISC {who}: max |d| {max(dd):.4f} (art only, tags out: {min(art):+.4f}..{max(art):+.4f}); disc {rng[0]:.3f}..{rng[1]:.3f}; "
          f">0.90 with {w90} / without {o90} of {len(fr)}; clip with max {max(v['disc'][who]['W']['clip'] for *_, v in fr):.3f} "
          f"without {max(v['disc'][who]['O']['clip'] for *_, v in fr):.3f}")
for aff in sorted(set(v["foeAff"] for *_, v in fr)):
    sub = [v for *_, v in fr if v["foeAff"] == aff]
    dd = [abs(v["disc"]["foe"]["W"]["mean"] - v["disc"]["foe"]["O"]["mean"]) for v in sub]
    art = [v["artDisc"]["foe"] for v in sub]
    print(f"  foe {aff:10s}: n {len(sub)} max |d| {max(dd):.4f} (art {min(art):+.4f}..{max(art):+.4f}); disc {min(v['disc']['foe']['W']['mean'] for v in sub):.3f}.."
          f"{max(v['disc']['foe']['W']['mean'] for v in sub):.3f}, contour {min(v['disc']['foe']['cW'] for v in sub):.3f}..{max(v['disc']['foe']['cW'] for v in sub):.3f}; "
          f">0.90 with {sum(1 for v in sub if v['disc']['foe']['W']['mean'] > 0.9)} without {sum(1 for v in sub if v['disc']['foe']['O']['mean'] > 0.9)}")
print("LEGIBILITY (median |dL| of the component's own pixels (min..max) [n frames]; out of a stop  /  in one):")
def leg(comp, states, nmin=20):
    a = [(v[comp]["dL"], v["stop"]) for *_, st, v in fr if st in states and v[comp]["n"] >= nmin]
    o = [x for x, s in a if not s]; i = [x for x, s in a if s]
    fmt = lambda b: f"{med(b):.3f} ({min(b):.3f}..{max(b):.3f}) [{len(b)}]" if b else "-"
    print(f"  {comp:10s} in {','.join(states):34s}: {fmt(o)}  /  {fmt(i)}")
leg("weaponBase", ["rest"]); leg("weapon", ["rest"])
leg("weaponBase", ["lit", "stop"]); leg("weapon", ["lit", "stop"])
leg("walls", ["cast"]); leg("walls", ["lit", "stop", "touch2", "touch10", "tstop"]); leg("walls", ["close", "over"])
leg("motes", ["lit", "stop", "touch2", "touch10"])
leg("head", ["cast", "lit", "stop", "touch2", "touch10", "tstop"]); leg("head", ["close", "over"])
leg("flare", ["touch0", "touch2", "tstop"])
leg("bolt", ["touch0"], nmin=5)
leg("streak", ["touch2", "touch10", "tstop"])
leg("tag", ["touch0", "touch2", "touch10", "tstop"])
leg("ground", ["cast", "lit", "stop", "touch0", "touch2", "touch10", "tstop", "close"])
leg("top", ["touch0"], nmin=5)
print("by state (median |dL| of everything the picture draws, the walls' tags included):")
for st in ["rest", "cast", "lit", "stop", "touch0", "touch2", "touch10", "tstop", "close", "over"]:
    a = [v["all"]["dL"] for *_, s, v in fr if s == st and v["all"]["n"] >= 20]
    n0 = sum(1 for *_, s, v in fr if s == st)
    if n0: print(f"  {st:8s} {med(a) if a else float('nan'):.3f} ({min(a) if a else float('nan'):.3f}..{max(a) if a else float('nan'):.3f}) n {len(a)} of {n0}"
                 f"  area {med([v['all']['areaU'] for *_, s, v in fr if s == st]):.0f} u2")
