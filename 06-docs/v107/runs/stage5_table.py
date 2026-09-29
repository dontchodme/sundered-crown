"""The stage-5 table (v107 §4) from the relic_rate jsons: both blocks, pooled, both sides."""
import json, pathlib
H = pathlib.Path(__file__).parent
def ld(p): return json.load(open(H / p))
rows = [("shipped nova (base)", "10.54", "ref_shipped_rr_{}.json")] + \
       [("Bulwark, stage 3 --set", b, f"stage5_rr_d{b}_{{}}.json") for b in ("9", "9.5", "10", "10.25", "10.5")] + \
       [("Bulwark, stage 3 as built", "10.54", "stage5_rr_d10.54_{}.json")] +        [("stage 5 link b9.5, no --set", "9.5", "stage5_rr_built_b9.5_{}.json"),
        ("first draft's b10, no --set", "10", "stage5_rr_built_b10_{}.json")]
print(f"{'':28}{'blade':>6} {'2207':>6} {'2317':>6} {'pooled':>7} {'side A':>7} {'side B':>7} {'mean s':>7} {'n':>5}")
for lab, b, pat in rows:
    j1, j2 = ld(pat.format(2207)), ld(pat.format(2317))
    g = j1["games"] + j2["games"]
    pooled = (j1["rate"] * j1["games"] + j2["rate"] * j2["games"]) / g
    sa = (j1["rateA"] + j2["rateA"]) / 2; sb = (j1["rateB"] + j2["rateB"]) / 2
    print(f"{lab:28}{b:>6} {100*j1['rate']:6.1f} {100*j2['rate']:6.1f} {100*pooled:7.1f} {100*sa:7.1f} {100*sb:7.1f} {(j1['dur']+j2['dur'])/2:7.1f} {g:5d}")
