"""v112 §4: the stage-5 table (both sides, two blocks, pooled; side A / side B), the pick in WINS, and the
ladder (by type and by foe) at the final and at the shipped relic, from runs/stage5_rr_*.json. Reads only.
    python stage5_table.py <S>"""
import json, math, pathlib, sys
R = pathlib.Path(sys.argv[1]) / "runs"
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
ROWS = [("shipped", "SHIPPED Rootfast (the freeze), 12.65, charge 15", "sc-tendril-t3 (the base)"),
        ("d10", "10     (charge 13)", "stage 3 --set dmg=10"), ("d10.5", "10.5   (charge 13)", "stage 3 --set dmg=10.5"),
        ("d11", "11     (charge 13)", "stage 3 --set dmg=11"),
        ("d11.5", "11.5   (charge 13) design's 'for 50' band", "stage 3 --set dmg=11.5"),
        ("d12", "12     (charge 13) design's 'for 50' band", "stage 3 --set dmg=12"),
        ("final", "12.65  (charge 13) design's 'leave it'", "sc-heartwood-rootfast (stage 3)"),
        ("c14", "12.65  charge 14 (the lab's 16)", "stage 3 --set ult.charge=14"),
        ("c15", "12.65  charge 15 (the shipped relic's)", "stage 3 --set ult.charge=15"),
        ("b11", "11     (charge 13) = THE FINAL", "sc-heartwood-b11 (stage 5)")]
L = ["point                                        block 2207  block 2317   pooled    wins/fights   side A   side B   mean dur   (link)"]
have = {}
for tag, lab, link in ROWS:
    rs = load(tag)
    if len(rs) < 2: L.append(f"{lab:<44} (not run)"); continue
    w, g, a, b, d = pooled(rs); have[tag] = (w, g)
    L.append(f"{lab:<44} {100*rs[0]['rate']:>6.1f}     {100*rs[1]['rate']:>6.1f}     {100*w/g:>6.1f}    {w:>5}/{g:<6}  {100*a:>6.1f}   {100*b:>6.1f}   {d:>6.1f}s   {link}")
extra = sorted(p.name for p in R.glob("stage5_rr_*_2207.json") if p.name[10:-10] not in {t for t, _, _ in ROWS})
for p in extra:
    tag = p.name[10:-10]; rs = load(tag)
    if len(rs) == 2:
        w, g, a, b, d = pooled(rs)
        L.append(f"{tag:<44} {100*rs[0]['rate']:>6.1f}     {100*rs[1]['rate']:>6.1f}     {100*w/g:>6.1f}    {w:>5}/{g:<6}  {100*a:>6.1f}   {100*b:>6.1f}   {d:>6.1f}s   {rs[0].get('set')}")
        have[tag] = (w, g)
L.append("")
dm = [(t, float(t[1:])) for t in have if t.startswith("d")] + ([("final", 12.65)] if "final" in have else [])
if dm:
    near = sorted(dm, key=lambda x: abs(have[x[0]][0] - have[x[0]][1] / 2))
    t, v = near[0]; w, g = have[t]
    se = math.sqrt(0.25 / g)
    L.append(f"THE 50% CROSSING (charge 13): the measured point nearest 50% is blade {v:g}: {w} of {g} = {100*w/g:.2f}% "
             f"(one SE {100*se:.2f} points); in wins from half: " + ", ".join(f"{x[1]:g} {have[x[0]][0] - have[x[0]][1]//2:+d}" for x in sorted(dm, key=lambda x: x[1])))
    pts = sorted((x[1], have[x[0]][0] / have[x[0]][1]) for x in dm)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if (y0 - 0.5) * (y1 - 0.5) <= 0 and y1 != y0:
            L.append(f"  linear between the bracketing points {x0:g} ({100*y0:.1f}) and {x1:g} ({100*y1:.1f}): {x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0):.2f}")
# THE STAGE-5 LINK IS THE MEASURED RELIC: relic_rate on sc-heartwood-b11 with NO --set against the
# final with --set dmg=11, block by block: the rate, every foe's rate, the side rates and the mean duration.
for b in ("2207", "2317"):
    p1, p2 = R / f"stage5_rr_b11_{b}.json", R / f"stage5_rr_d11_{b}.json"
    if p1.exists() and p2.exists():
        x, y = json.loads(p1.read_text()), json.loads(p2.read_text())
        same = [k for k in ("rate", "rateA", "rateB", "dur", "games", "timeouts") if x[k] == y[k]]
        foes = sum(x["byFoe"][f] == y["byFoe"].get(f) for f in x["byFoe"])
        ok = len(same) == 6 and foes == len(x["byFoe"]) == len(y["byFoe"])
        L.append(f"PROOF block {b}: sc-heartwood-b11 (no --set) {100*x['rate']:.2f}% mean {x['dur']:.4f}s  vs  stage 3 --set dmg=11 "
                 f"{100*y['rate']:.2f}% mean {y['dur']:.4f}s; foes identical {foes}/{len(x['byFoe'])}; "
                 f"rate/sides/dur/timeouts identical {len(same)}/6 -> " + ("EXACTLY THE SAME" if ok else "DIFFERENT"))
if "shipped" in have:
    w, g = have["shipped"]; L.append(f"THE SHIPPED REFERENCE: Heartwood as shipped on the base, {w} of {g} = {100*w/g:.2f}% both sides")
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
L += ladder("b11", "LADDER -- Heartwood / Rootfast REDESIGNED, THE FINAL (sc-heartwood-b11: charge 13, blade 11 -- Rick's ruling, nearest 50%), both sides")
L += ladder("final", "LADDER -- the design's own 'leave the blade', 12.65 (sc-heartwood-rootfast, stage 3: charge 13), both sides")
L += ladder("shipped", "LADDER -- Heartwood as SHIPPED (sc-tendril-t3: the freeze, charge 15, blade 12.65), both sides")
text = "\n".join(L) + "\n"
(R / "stage5_table.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
