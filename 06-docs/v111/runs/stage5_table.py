"""The stage-5 table from relic_rate jsons (both sides, 740 fights a block, two blocks), in wins,
against the shipped rate (Spellbreaker as shipped on the base: the bolt at 8.81, charge 13) and 50%."""
import json, glob, os, re, sys
S = sys.argv[1]
def load(tag):
    out = []
    for B in ("2207", "2317"):
        p = f"{S}/{tag}_{B}.json"
        if not os.path.exists(p): return None
        out.append(json.load(open(p)))
    return out
def row(label, js, ref=None):
    a, b = js
    wa, wb = round(a["rate"] * a["games"]), round(b["rate"] * b["games"])
    g = a["games"] + b["games"]; w = wa + wb
    sA = (a["rateA"] * a["games"] / 2 + b["rateA"] * b["games"] / 2) / (g / 2)
    sB = (a["rateB"] * a["games"] / 2 + b["rateB"] * b["games"] / 2) / (g / 2)
    dur = (a["dur"] + b["dur"]) / 2
    extra = ""
    if ref is not None: extra = f"   {w - ref:+4d} wins vs shipped   {w - g // 2:+4d} vs 50%"
    print(f"{label:<36} {100*a['rate']:5.1f}   {100*b['rate']:5.1f}   {100*abs(a['rate']-b['rate']):4.1f}   {100*w/g:5.1f} ({w}/{g})"
          f"   {100*sA:5.1f}   {100*sB:5.1f}   {dur:5.1f}s{extra}")
    return w
print(f"{'blade':<36} {'blk 1':>5}   {'blk 2':>5}   {'split':>4}   {'pooled (wins)':<16}  {'sideA':>5}   {'sideB':>5}   mean")
ref = row("8.81 SHIPPED (the bolt): the target", load("rr_shipped"))
pts = sorted({re.search(r"stage5_rr_d([\d.]+)_\d+\.json$", p).group(1) for p in glob.glob(f"{S}/stage5_rr_d*_*.json")}, key=float, reverse=True)
for x in pts:
    js = load(f"stage5_rr_d{x}")
    if js: row(f"{x}" + ("  (the brief's grid)" if x in ("8.3", "8.5", "8.8") else "  (the stage-3 link)" if x == "8.81" else ""), js, ref)
for p in sorted(glob.glob(f"{S}/stage5_rr_link_*_2207.json")):
    t = os.path.basename(p)[:-10]; js = load(t)
    if js: row(f"{t.replace('stage5_rr_', '')}  (the stage-5 link, no --set)", js, ref)
