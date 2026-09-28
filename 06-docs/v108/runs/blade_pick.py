# The stage-5 pick in WINS, not rounded percentages: every measured blade's wins of 1480 (both sides,
# two blocks) against the shipped relic's, nearest first. Reads runs/stage5_rr_*.json only.
import json, math, sys, pathlib
R = pathlib.Path(sys.argv[1])
def wins(tag):
    w = g = 0
    for b in ("2207", "2317"):
        j = json.loads((R / f"stage5_rr_{tag}_{b}.json").read_text())
        w += round(j["rate"] * j["games"]); g += j["games"]
    return w, g
sw, sg = wins("shipped")
se = math.sqrt((sw / sg) * (1 - sw / sg) / sg)
print(f"THE TARGET (v83 §5 stage 3, 'to the shipped rate'): Ironhail as shipped on sc-tendril-t3, relic_rate both sides,")
print(f"seed0 2207 + 2317: {sw} wins of {sg} = {100*sw/sg:.2f}%  (one SE {100*se:.2f} points = {se*sg:.1f} wins)\n")
rows = []
for tag, lab in (("d12", "12"), ("d13", "13"), ("d14", "14"), ("d14.5", "14.5"), ("d15", "15  (grid)"), ("d15.5", "15.5 (grid)"),
                 ("d16", "16  (grid)"), ("d16.23", "16.23 (shipped blade = sc-ironhail-sunder)"), ("d16.5", "16.5")):
    w, g = wins(tag); rows.append((abs(w - sw), w - sw, w, g, lab))
print("blade                                        wins/1480   rate     vs shipped")
for d, dd, w, g, lab in sorted(rows):
    print(f"  {lab:<42} {w:>5}      {100*w/g:5.2f}%   {dd:+d} wins ({100*dd/g:+.2f})")
best = min(r[0] for r in rows)
tie = [r[4] for r in rows if r[0] == best]
print(f"\nnearest the shipped rate: {' and '.join(tie)}  ({'AN EXACT TIE' if len(tie) > 1 else 'unique'}, {best} wins off)")
w50 = sorted(rows, key=lambda r: abs(r[2] - r[3] / 2))[0]
print(f"nearest 50% (Rick's other choice): {w50[4]}  {w50[2]} of {w50[3]} = {100*w50[2]/w50[3]:.2f}%")
