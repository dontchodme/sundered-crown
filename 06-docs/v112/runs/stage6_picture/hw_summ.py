"""Summarise hw_measure.py output: the gates and the controls. usage: hw_summ.py m1.json [...]. SCRATCH."""
import sys, json, pathlib
HERE = pathlib.Path(__file__).parent
R = []
for a in sys.argv[1:]:
    p = pathlib.Path(a); p = p if p.is_absolute() else HERE / p
    R += json.loads(p.read_text())
states = []
for f in R:
    for st, v in f["got"].items():
        v["_f"] = f"{f['foe']}/{f['seed']}{f['side']}"; states.append(v)
print(f"{len(R)} fights, {len(states)} measured frames; missing: " + ", ".join(f"{f['foe']}:{'/'.join(f['missing'])}" for f in R if f["missing"]))
mx = lambda xs: max(xs) if xs else float("nan")
mn = lambda xs: min(xs) if xs else float("nan")
# BLOOM
dl = [v["arena"]["dLift"] for v in states]
worst = max(states, key=lambda v: v["arena"]["dLift"])
print(f"\nBLOOM: the picture's share of the arena lift: max {mx(dl):+.4f} ({worst['_f']} {worst['st']}), min {mn(dl):+.4f}   (gate <= +0.02)")
print(f"  raw luma the picture adds (chain on): max {mx([v['arena']['picOn'] for v in states]):+.4f}; clip with {mx([v['arena']['clipW'] for v in states]):.4f} without {mx([v['arena']['clipO'] for v in states]):.4f}")
# DISCS
for who in ("me", "foe"):
    d = [v["artDisc"][who] for v in states]
    w = max(states, key=lambda v: abs(v["artDisc"][who]))
    o90 = [v["artDisc"][who + "90"] for v in states]
    clipd = [v["artDisc"][who + "Clip"] for v in states]
    base90 = [v["disc"][who]["O"]["over90"] for v in states]
    print(f"DISC {who:3s}: art moves the disc mean by {mn(d):+.4f}..{mx(d):+.4f} (worst {w['_f']} {w['st']} {w['foeAff'] if who == 'foe' else ''}); "
          f">0.90 share max {mx(o90):.3f} (without the art {mx(base90):.3f}); clip max {mx(clipd):.4f}")
by = {}
for v in states: by.setdefault(v["foeAff"], []).append(v["artDisc"]["foe"])
print("  foe disc by school: " + "  ".join(f"{k} {mn(x):+.4f}..{mx(x):+.4f}" for k, x in sorted(by.items())))
# CONTROLS
for c in (1, 2, 3):
    k = "ctrl" + str(c)
    cs = [v for v in states if k in v]
    dls = [v[k]["dLift"] for v in cs]
    me90 = [v[k]["me"]["over90"] for v in cs]; foe90 = [v[k]["foe"]["over90"] for v in cs]
    fail_l = sum(1 for x in dls if x > 0.02)
    fail_me = sum(1 for v in cs if v[k]["me"]["over90"] > 0.5); fail_foe = sum(1 for v in cs if v[k]["foe"]["over90"] > 0.5)
    print(f"CONTROL {c}: dLift max {mx(dls):+.4f} (> +0.02 on {fail_l}/{len(cs)}); caster disc >0.90 on >half the disc {fail_me}/{len(cs)}; "
          f"foe disc {fail_foe}/{len(cs)}")
# LEGIBILITY
print("\nLEGIBILITY (|dL| of the pixels a component moves by > 0.02; n px at 540x960) -- out of / in a hit stop:")
comps = ["blade", "green", "scale", "front", "ground", "motes", "bits", "root", "tag", "all"]
for c in comps:
    row = []
    for stop in (False, True):
        xs = [v[c] for v in states if c in v and v["stop"] == stop and v[c]["n"] > 0]
        if xs:
            row.append(f"{'stop' if stop else 'free'}: dL med {sorted(x['dL'] for x in xs)[len(xs)//2]:.3f} min {mn([x['dL'] for x in xs]):.3f} "
                       f"dE med {sorted(x.get('dE', 0) for x in xs)[len(xs)//2]:4.1f} "
                       f"n med {sorted(x['n'] for x in xs)[len(xs)//2]:5d} ({len(xs)} frames)")
        else:
            row.append(f"{'stop' if stop else 'free'}: --")
    print(f"  {c:7s} " + " | ".join(row))
print("\nPER STATE (median |dL| of the whole picture, frames):")
for st in ["rest", "cast", "caststop", "green", "sprout", "window", "stop", "root", "held", "wilt", "reroot", "close", "over"]:
    xs = [v for v in states if v["st"] == st]
    if not xs: print(f"  {st:7s} --"); continue
    al = sorted(v["all"]["dL"] for v in xs)
    print(f"  {st:7s} {len(xs):2d} frames: all dL med {al[len(al)//2]:.3f} n med {sorted(v['all']['n'] for v in xs)[len(xs)//2]:5d}; "
          f"dLift max {mx([v['arena']['dLift'] for v in xs]):+.4f}; foe disc art {mn([v['artDisc']['foe'] for v in xs]):+.4f}..{mx([v['artDisc']['foe'] for v in xs]):+.4f}; "
          f"me {mn([v['artDisc']['me'] for v in xs]):+.4f}..{mx([v['artDisc']['me'] for v in xs]):+.4f}")
