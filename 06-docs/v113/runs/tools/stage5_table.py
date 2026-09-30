"""v113 §4: the stage-5 table (both sides, two blocks, pooled; side A / side B), the pick in WINS (nearest 50%,
Rick's ruling; and the design's own target, the shipped rate on 151, beside it), the proof that the stage-5 link
is the measured relic, and the ladders (by type and by foe) at the final, at the design's blade and at the shipped
relic, from runs/stage5_rr_*.json. Reads only.    python stage5_table.py <S> [final blade]"""
import json, math, pathlib, sys
R = pathlib.Path(sys.argv[1]) / "runs"
FB = sys.argv[2] if len(sys.argv) > 2 else None
def load(tag):
    out = []
    for b in ("2207", "2317"):
        p = R / f"stage5_rr_{tag}_{b}.json"
        if p.exists(): out.append(json.loads(p.read_text()))
    return out
def pooled(rs):
    g = sum(r["games"] for r in rs)
    w = sum(round(r["rate"] * r["games"]) for r in rs)
    return (w, g, sum(r["rateA"] * r["games"] / 2 for r in rs) / (g / 2),
            sum(r["rateB"] * r["games"] / 2 for r in rs) / (g / 2), sum(r["dur"] * r["games"] for r in rs) / g)
tags = sorted({p.name[len("stage5_rr_"):-len("_2207.json")] for p in R.glob("stage5_rr_*_2207.json")})
ds = sorted([t for t in tags if t.startswith("d")], key=lambda t: float(t[1:]))
ROWS = [("shipped", "SHIPPED Bramblesnare (the 1.6s root), 31.35, ch 15", "sc-tendril-t3 (the base)")]
ROWS += [(t, f"{t[1:]:<6} (charge 14)", f"stage 3 --set dmg={t[1:]}") for t in ds]
ROWS += [("final3135", "31.35  (charge 14) the shipped blade", "sc-thornwake-snare (stage 3)")]
if FB: ROWS += [(f"b{FB}", f"{FB:<6} (charge 14) = THE FINAL", f"sc-thornwake-b{FB} (stage 5)")]
L = ["point                                          block 2207  block 2317   pooled    wins/fights   side A   side B   mean dur   (link)"]
have = {}
for tag, lab, link in ROWS:
    rs = load(tag)
    if len(rs) < 2: L.append(f"{lab:<46} (not run)"); continue
    w, g, a, b, d = pooled(rs); have[tag] = (w, g)
    L.append(f"{lab:<46} {100*rs[0]['rate']:>6.1f}     {100*rs[1]['rate']:>6.1f}     {100*w/g:>6.1f}    {w:>5}/{g:<6}  {100*a:>6.1f}   {100*b:>6.1f}   {d:>6.1f}s   {link}")
L.append("")
dm = [(t, float(t[1:])) for t in have if t.startswith("d")] + ([("final3135", 31.35)] if "final3135" in have else [])
def cross(target, name):
    near = sorted(dm, key=lambda x: abs(have[x[0]][0] - target * have[x[0]][1]))
    t, v = near[0]; w, g = have[t]
    out = [f"{name}: the measured point nearest {100*target:.2f}% is blade {v:g}: {w} of {g} = {100*w/g:.2f}% "
           f"(one SE {100*math.sqrt(0.25/g):.2f} points); in wins from the target: "
           + ", ".join(f"{x[1]:g} {have[x[0]][0] - target * have[x[0]][1]:+.0f}" for x in sorted(dm, key=lambda x: x[1]))]
    pts = sorted((x[1], have[x[0]][0] / have[x[0]][1]) for x in dm)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if (y0 - target) * (y1 - target) <= 0 and y1 != y0:
            out.append(f"  linear between the bracketing points {x0:g} ({100*y0:.1f}) and {x1:g} ({100*y1:.1f}): {x0 + (target - y0) * (x1 - x0) / (y1 - y0):.2f}")
    return out
if dm:
    L += cross(0.5, "THE 50% CROSSING (Rick's ruling, charge 14)")
    if "shipped" in have:
        w, g = have["shipped"]
        L.append(f"THE SHIPPED REFERENCE: Thornwake as shipped on the base (the freeze), {w} of {g} = {100*w/g:.2f}% both sides")
        L += cross(w / g, "THE DESIGN'S OWN TARGET (the shipped rate on 151)")
if FB:
    for b in ("2207", "2317"):
        p1, p2 = R / f"stage5_rr_b{FB}_{b}.json", R / f"stage5_rr_d{FB}_{b}.json"
        if p1.exists() and p2.exists():
            x, y = json.loads(p1.read_text()), json.loads(p2.read_text())
            same = [k for k in ("rate", "rateA", "rateB", "dur", "games", "timeouts") if x[k] == y[k]]
            foes = sum(x["byFoe"][f] == y["byFoe"].get(f) for f in x["byFoe"])
            ok = len(same) == 6 and foes == len(x["byFoe"]) == len(y["byFoe"])
            L.append(f"PROOF block {b}: sc-thornwake-b{FB} (no --set) {100*x['rate']:.2f}% mean {x['dur']:.4f}s  vs  stage 3 --set dmg={FB} "
                     f"{100*y['rate']:.2f}% mean {y['dur']:.4f}s; foes identical {foes}/{len(x['byFoe'])}; "
                     f"rate/sides/dur/timeouts identical {len(same)}/6 -> " + ("EXACTLY THE SAME" if ok else "DIFFERENT"))
def ladder(tag, title):
    rs = load(tag)
    if len(rs) < 2: return []
    w, g, *_ = pooled(rs)
    out = ["", title, f"(40 fights a foe: 10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317). Pooled: {100*w/g:.1f}%"]
    types = {t: sum(r["byType"][t] for r in rs) / 2 for t in rs[0]["byType"]}
    out.append("by type  " + "  ".join(f"{t} {100*v:.0f}%" for t, v in sorted(types.items(), key=lambda kv: -kv[1])))
    foes = {f: sum(r["byFoe"][f] for r in rs) / 2 for f in rs[0]["byFoe"]}
    srt = sorted(foes.items(), key=lambda kv: (kv[1], kv[0]))
    out.append("by foe   " + "  ".join(f"{f} {100*v:.1f}" for f, v in srt))
    return out
if FB: L += ladder(f"b{FB}", f"LADDER -- Thornwake / Bramblesnare REDESIGNED, THE FINAL (sc-thornwake-b{FB}: charge 14, blade {FB} -- Rick's ruling, nearest 50%), both sides")
L += ladder("final3135", "LADDER -- the redesign at the shipped blade 31.35 (sc-thornwake-snare, stage 3: charge 14), both sides")
L += ladder("shipped", "LADDER -- Thornwake as SHIPPED (sc-tendril-t3: the freeze, charge 15, blade 31.35), both sides")
text = "\n".join(L) + "\n"
(R / "stage5_table.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
