"""Summarise tw_measure.py's json: bloom share (the whole picture; the floor alone), discs by foe school, the controls,
legibility by component (in / out of a stop), and by state. usage: tw_summ.py m1.json"""
import sys, json, statistics as S
d = json.load(open(sys.argv[1]))
fr = [(x["foe"], x["seed"], x["side"], k, v) for x in d for k, v in x["got"].items()]
print(f"{len(fr)} frames, {len(d)} fights; missing: " + "; ".join(f"{x['foe']} {x['seed']}{x['side']} {x['missing']}" for x in d if x["missing"]))
med = lambda a: S.median(a) if a else float("nan")
dl = [v["arena"]["dLift"] for *_, v in fr]
fl = [v["arena"]["floorLift"] for *_, v in fr]
pic = [v["arena"]["picOn"] for *_, v in fr]
raw = [v["arena"]["floorRaw"] for *_, v in fr]
worst = max(fr, key=lambda z: z[4]["arena"]["dLift"])
wf = max(fr, key=lambda z: z[4]["arena"]["floorLift"])
print(f"BLOOM: the picture's share of the chain's arena lift max {max(dl):+.4f} min {min(dl):+.4f} (gate +0.02) "
      f"[worst {worst[0]} {worst[1]}{worst[2]} {worst[3]}]; raw luma added (chain on) max {max(pic):+.4f} min {min(pic):+.4f}; "
      f"arena clip with max {max(v['arena']['clipW'] for *_, v in fr):.4f} without {max(v['arena']['clipO'] for *_, v in fr):.4f}")
print(f"  THE FLOOR ALONE (drawBrier hidden vs shown): its share of the lift max {max(fl):+.4f} min {min(fl):+.4f} "
      f"[worst {wf[0]} {wf[1]}{wf[2]} {wf[3]}]; the raw luma it adds (chain off) max {max(raw):+.4f} min {min(raw):+.4f}")
for c, what in (("ctrl1", "a white lighter wash r 300 at every bramble (the Harrowing class: reach)"),
                ("ctrl2", "a white-hot lighter glow on the caster while the blade is green"),
                ("ctrl3", "the snare as a filled white lighter disc over the held foe")):
    cd = [v[c]["dLift"] for *_, v in fr]
    fails = sum(1 for a in cd if a > 0.02); fails1 = sum(1 for a in cd if a > 0.01)
    fw = [v for *_, v in fr if v["green"] > 0 and not v["over"] and v["meAlive"]]
    me90 = sum(1 for v in fw if v[c]["me"]["mean"] > 0.90 and v["disc"]["me"]["O"]["mean"] <= 0.90)
    fon = [v for *_, v in fr if v["rootFade"] > 0.01 and v["foeAlive"]]
    fo90 = sum(1 for v in fon if v[c]["foe"]["mean"] > 0.90 and v["disc"]["foe"]["O"]["mean"] <= 0.90)
    fall = [v for *_, v in fr if v["foeAlive"]]
    fa90 = sum(1 for v in fall if v[c]["foe"]["mean"] > 0.90 and v["disc"]["foe"]["O"]["mean"] <= 0.90)
    print(f"  CONTROL {c} ({what}): dLift max {max(cd):+.4f}, > 0.02 on {fails}/{len(fr)}, > 0.01 on {fails1}/{len(fr)}; "
          f"caster disc pushed past 0.90 on {me90}/{len(fw)} green frames; foe disc pushed past 0.90 on {fo90}/{len(fon)} "
          f"snared frames, {fa90}/{len(fall)} of all (max caster {max(v[c]['me']['mean'] for *_, v in fr):.3f}, foe {max(v[c]['foe']['mean'] for *_, v in fr):.3f})")
for who in ("me", "foe"):
    dd = [abs(v["disc"][who]["W"]["mean"] - v["disc"][who]["O"]["mean"]) for *_, v in fr]
    w90 = sum(1 for *_, v in fr if v["disc"][who]["W"]["mean"] > 0.90); o90 = sum(1 for *_, v in fr if v["disc"][who]["O"]["mean"] > 0.90)
    art = [v["artDisc"][who] for *_, v in fr]
    wa = max(fr, key=lambda z: abs(z[4]["artDisc"][who]))
    rng = (min(v["disc"][who]["W"]["mean"] for *_, v in fr), max(v["disc"][who]["W"]["mean"] for *_, v in fr))
    print(f"DISC {who}: max |d| {max(dd):.4f} (art only, tags out: {min(art):+.4f}..{max(art):+.4f} [largest {wa[0]} {wa[1]}{wa[2]} {wa[3]}]); "
          f"disc {rng[0]:.3f}..{rng[1]:.3f}; >0.90 with {w90} / without {o90} of {len(fr)}; clip with max "
          f"{max(v['disc'][who]['W']['clip'] for *_, v in fr):.3f} without {max(v['disc'][who]['O']['clip'] for *_, v in fr):.3f}")
for aff in sorted(set(v["foeAff"] for *_, v in fr)):
    sub = [v for *_, v in fr if v["foeAff"] == aff and v["foeAlive"]]
    if not sub: continue
    art = [abs(v["artDisc"]["foe"]) for v in sub]
    print(f"  foe {aff:10s}: n {len(sub)} art max |d| {max(art):.4f}; disc {min(v['disc']['foe']['W']['mean'] for v in sub):.3f}.."
          f"{max(v['disc']['foe']['W']['mean'] for v in sub):.3f}, contour {min(v['disc']['foe']['cW'] for v in sub):.3f}..{max(v['disc']['foe']['cW'] for v in sub):.3f} "
          f"(without {min(v['disc']['foe']['cO'] for v in sub):.3f}..{max(v['disc']['foe']['cO'] for v in sub):.3f}); "
          f">0.90 with {sum(1 for v in sub if v['disc']['foe']['W']['mean'] > 0.9)} without {sum(1 for v in sub if v['disc']['foe']['O']['mean'] > 0.9)}")
sub = [v for *_, v in fr if v["meAlive"]]
print(f"  caster (verdant): n {len(sub)} art max |d| {max(abs(v['artDisc']['me']) for v in sub):.4f}; disc {min(v['disc']['me']['W']['mean'] for v in sub):.3f}.."
      f"{max(v['disc']['me']['W']['mean'] for v in sub):.3f}")
print("LEGIBILITY (median |dL| of the component's own pixels (min..max) [n frames]; out of a stop  /  in one):")
def leg(comp, states, nmin=20):
    a = [(v[comp]["dL"], v["stop"]) for *_, st, v in fr if st in states and v[comp]["n"] >= nmin]
    o = [x for x, s in a if not s]; i = [x for x, s in a if s]
    fmt = lambda b: f"{med(b):.3f} ({min(b):.3f}..{max(b):.3f}) [{len(b)}]" if b else "-"
    print(f"  {comp:6s} in {','.join(states):40s}: {fmt(o)}  /  {fmt(i)}")
    return o, i
WIN = ["plant", "off", "in", "snare", "bite", "stop", "stopoff"]
leg("floor", WIN + ["after", "brown"])
leg("tangle", WIN + ["after"])
leg("tangle", ["plant"])
leg("tangle", ["brown"])
leg("shade", WIN + ["after", "brown"])
leg("motes", WIN + ["after", "brown"])
leg("root", ["snare"])
leg("root", ["bite", "in", "stop", "plant"])
leg("top", ["snare", "bite", "stop", "plant"])
leg("bite", ["bite"])
leg("blade", ["cast", "green", "plant", "off", "in", "snare", "bite", "stop", "stopoff"])
leg("blade", ["close"])
leg("tag", ["bite", "in", "snare", "stop", "plant"])
print("by state (median |dL| of everything the picture draws, its tags included):")
for st in ["rest", "cast", "green", "plant", "off", "in", "snare", "bite", "stop", "stopoff", "close", "after", "brown", "over"]:
    a = [v["all"]["dL"] for *_, s, v in fr if s == st and v["all"]["n"] >= 20]
    n0 = sum(1 for *_, s, v in fr if s == st)
    if n0: print(f"  {st:7s} {med(a) if a else float('nan'):.3f} ({min(a) if a else float('nan'):.3f}..{max(a) if a else float('nan'):.3f}) n {len(a)} of {n0}"
                 f"  [pixels moved: med {med([v['all']['n'] for *_, s, v in fr if s == st])}]")
