"""v108 §4 (after the review): the stage-5 table (pooled both blocks, side A / side B), the proof
that the final link is the measured relic, and the ladder at THE FINAL (blade 16.23, the shipped
rate) by type and by foe beside the shipped relic and the 50% alternative (blade 14). Reads only
the relic_rate jsons in runs/."""
import json, math, pathlib, sys
S = pathlib.Path(sys.argv[1]) / "runs"
def load(tag):
    return [json.loads((S / f"stage5_rr_{tag}_{b}.json").read_text()) for b in ("2207", "2317")]
def pooled(rs):
    g = sum(r["games"] for r in rs)
    return (sum(r["rate"] * r["games"] for r in rs) / g,
            sum(r["rateA"] * r["games"] / 2 for r in rs) / (g / 2),
            sum(r["rateB"] * r["games"] / 2 for r in rs) / (g / 2), g,
            sum(r["dur"] * r["games"] for r in rs) / g)
out = ["blade                       block 2207   block 2317   split   pooled   side A   side B   fights   mean dur   (link)"]
rows = [("shipped", "16.23 SHIPPED (the nova)", "sc-tendril-t3: THE REFERENCE"),
        ("d15", "15     (the brief's grid)", "sc-ironhail-sunder --set dmg"),
        ("d15.5", "15.5   (the brief's grid)", "sc-ironhail-sunder --set dmg"),
        ("d16", "16     (the brief's grid)", "sc-ironhail-sunder --set dmg"),
        ("d16.23", "16.23  FINAL, the link", "sc-ironhail-sunder, no --set"),
        ("set16.23", "16.23  --set (the proof)", "sc-ironhail-sunder --set dmg=16.23"),
        ("d16.5", "16.5   (above the bow row)", "sc-ironhail-sunder --set dmg"),
        ("d12", "12", "sc-ironhail-sunder --set dmg"), ("d13", "13", "sc-ironhail-sunder --set dmg"),
        ("d14", "14     (50% alternative)", "sc-ironhail-sunder --set dmg"),
        ("d14.5", "14.5", "sc-ironhail-sunder --set dmg"),
        ("built_b14", "14     ALT BUILT", "sc-ironhail-b14, no --set")]
wide = []
for tag, lab, link in rows:
    rs = load(tag); p, a, b, g, d = pooled(rs)
    sp = abs(rs[0]["rate"] - rs[1]["rate"]) * 100
    if sp > 5: wide.append(f"{lab.split()[0]} ({100*rs[0]['rate']:.1f} / {100*rs[1]['rate']:.1f}, {sp:.1f} apart)")
    out.append(f"{lab:<28}{100*rs[0]['rate']:>8.1f}   {100*rs[1]['rate']:>10.1f}   {sp:>5.1f}   {100*p:>6.1f}   "
               f"{100*a:>6.1f}   {100*b:>6.1f}   {g:>6}   {d:>6.1f}s   {link}")
ship = pooled(load("shipped"))[0]
se = math.sqrt(ship * (1 - ship) / 1480)
out.append("")
out.append(f"the shipped rate {100*ship:.1f}% (1480 fights, one SE {100*se:.2f} points); block splits over 5 points: "
           + ("; ".join(wide) if wide else "none"))
# THE PROOF: the final link with no --set is the --set run, block for block, foe for foe
proof = []
for b, x, y in zip(("2207", "2317"), load("d16.23"), load("set16.23")):
    same = (x["rate"] == y["rate"] and x["rateA"] == y["rateA"] and x["rateB"] == y["rateB"]
            and x["dur"] == y["dur"] and x["byFoe"] == y["byFoe"] and x["byType"] == y["byType"]
            and x["games"] == y["games"])
    proof.append(f"block {b}: link {100*x['rate']:.1f}% (A {100*x['rateA']:.1f} B {100*x['rateB']:.1f}, {x['dur']:.4f}s) "
                 f"vs --set dmg=16.23 {100*y['rate']:.1f}% (A {100*y['rateA']:.1f} B {100*y['rateB']:.1f}, {y['dur']:.4f}s): "
                 f"{'IDENTICAL (rate, both sides, duration, all ' + str(len(x['byFoe'])) + ' foes, every type)' if same else 'DIFFERENT'}")
out += ["", "THE FINAL LINK IS THE MEASURED RELIC:"] + ["  " + p for p in proof]
def ladder(tag):
    rs = load(tag)
    types = {t: sum(r["byType"][t] for r in rs) / 2 for t in rs[0]["byType"]}
    foes = {f: sum(r["byFoe"][f] for r in rs) / 2 for f in rs[0]["byFoe"]}
    return pooled(rs)[0], types, foes
pf, tf, ff = ladder("d16.23"); ps, ts, fs = ladder("shipped"); pa, ta, fa = ladder("d14")
L = ["", "THE LADDER AT THE FINAL: Ironhail / Quarrelstorm REDESIGNED (sc-ironhail-sunder: the hail + sunder, blade 16.23)",
     "win by foe, both sides, 40 fights a foe (10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317),",
     f"beside Ironhail as SHIPPED (sc-tendril-t3: the nova, 16.23) and the 50% alternative (blade 14). "
     f"Pooled: final {100*pf:.1f}%, shipped {100*ps:.1f}%, alt {100*pa:.1f}%", "",
     "by type           final   shipped   alt 14"]
for t in sorted(tf, key=lambda t: -tf[t]):
    L.append(f"  {t:<14}{100*tf[t]:>6.0f}%   {100*ts[t]:>6.0f}%   {100*ta[t]:>5.0f}%")
L += ["", "by foe            final   shipped   alt 14   (final - shipped)"]
for f in sorted(ff, key=lambda f: (ff[f], f)):
    L.append(f"  {f:<14}{100*ff[f]:>6.1f}%  {100*fs[f]:>6.1f}%  {100*fa[f]:>6.1f}%   {100*(ff[f]-fs[f]):+6.1f}")
text = "\n".join(out + L) + "\n"
(S / "ladder_final.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
