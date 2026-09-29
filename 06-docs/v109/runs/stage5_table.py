"""The stage-5 table (v109 §4) from the relic_rate jsons: both blocks, pooled, both sides; the line through the grid."""
import json, pathlib
H = pathlib.Path(__file__).parent
def ld(p): return json.load(open(H / p))
grid = ("24", "24.5", "25", "25.5", "26", "26.5", "27")
rows = [("the shipped nova (the base)", "28.77", "ref_shipped_rr_{}.json")] + \
       [("Consecration, stage 3 --set", b, f"stage5_rr_d{b}_{{}}.json") for b in grid] + \
       [("Consecration, stage 3 as built", "28.77", "stage5_rr_d28.77_{}.json"),
        ("sc-censer-consecration-b25.5, no set", "25.5", "stage5_rr_built_b25.5_{}.json")]
print(f"{'':38}{'blade':>6} {'2207':>6} {'2317':>6} {'pooled':>7} {'side A':>7} {'side B':>7} {'mean s':>7} {'n':>5}")
P = {}
for lab, b, pat in rows:
    j1, j2 = ld(pat.format(2207)), ld(pat.format(2317))
    g = j1["games"] + j2["games"]
    pooled = (j1["rate"] * j1["games"] + j2["rate"] * j2["games"]) / g
    sa = (j1["rateA"] + j2["rateA"]) / 2; sb = (j1["rateB"] + j2["rateB"]) / 2
    if "--set" in lab: P[float(b)] = 100 * pooled
    if "shipped" in lab: ref = 100 * pooled
    print(f"{lab:38}{b:>6} {100*j1['rate']:6.1f} {100*j2['rate']:6.1f} {100*pooled:7.2f} {100*sa:7.1f} {100*sb:7.1f} {(j1['dur']+j2['dur'])/2:7.1f} {g:5d}")
xs, ys = list(P), list(P.values()); n = len(xs); mx, my = sum(xs) / n, sum(ys) / n
b = sum((x - mx) * (y - my) for x, y in P.items()) / sum((x - mx) ** 2 for x in xs); a = my - b * mx
print(f"\nthe line through the seven: {a:.2f} + {b:.2f} x blade; the shipped {ref:.2f} at {(ref - a) / b:.2f}, 50% at {(50 - a) / b:.2f}")
near = min(P, key=lambda x: abs(P[x] - ref)); near50 = min(P, key=lambda x: abs(P[x] - 50))
print(f"the measured point nearest the shipped rate: {near:g} ({P[near]:.2f}, {P[near] - ref:+.2f}); nearest 50%: {near50:g} ({P[near50]:.2f})")
print("residuals: " + "  ".join(f"{x:g} {y - (a + b * x):+.2f}" for x, y in P.items()))
