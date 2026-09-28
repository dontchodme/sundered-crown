"""v108 §4: the stage-5 table (pooled both blocks, side A / side B) and the ladder at the taken blade
and at the shipped relic, by type and by foe, from the relic_rate jsons in runs/. Reads only."""
import json, pathlib, sys
S = pathlib.Path(sys.argv[1]) / "runs"
def load(tag):
    return [json.loads((S / f"stage5_rr_{tag}_{b}.json").read_text()) for b in ("2207", "2317")]
def pooled(rs):
    g = sum(r["games"] for r in rs)
    return (sum(r["rate"] * r["games"] for r in rs) / g,
            sum(r["rateA"] * r["games"] / 2 for r in rs) / (g / 2),
            sum(r["rateB"] * r["games"] / 2 for r in rs) / (g / 2), g,
            sum(r["dur"] * r["games"] for r in rs) / g)
out = []
out.append("blade   block 2207   block 2317   pooled   side A   side B   fights   mean dur   (link)")
for tag, lab, link in [("shipped", "16.23 SHIPPED (the nova)", "sc-tendril-t3"),
                       ("d12", "12", "sc-ironhail-sunder --set"), ("d13", "13", "sc-ironhail-sunder --set"),
                       ("d14", "14", "sc-ironhail-sunder --set"), ("d14.5", "14.5", "sc-ironhail-sunder --set"),
                       ("d15", "15", "sc-ironhail-sunder --set"), ("d15.5", "15.5", "sc-ironhail-sunder --set"),
                       ("d16", "16", "sc-ironhail-sunder --set"), ("d16.23", "16.23 (kept)", "sc-ironhail-sunder"),
                       ("d16.5", "16.5", "sc-ironhail-sunder --set"), ("built_b14", "14 BUILT", "sc-ironhail-b14, no --set")]:
    rs = load(tag); p, a, b, g, d = pooled(rs)
    out.append(f"{lab:<26}{100*rs[0]['rate']:>6.1f}   {100*rs[1]['rate']:>6.1f}   {100*p:>6.1f}   {100*a:>6.1f}   {100*b:>6.1f}   {g:>6}   {d:>6.1f}s   {link}")
def ladder(tag, title):
    rs = load(tag)
    L = [title, f"(40 fights a foe: 10 seeds x 2 sides x 2 blocks, relic_rate seed0 2207 + 2317). Pooled: {100*pooled(rs)[0]:.1f}%", ""]
    types = {}
    for t in rs[0]["byType"]:
        types[t] = sum(r["byType"][t] for r in rs) / 2
    L.append("by type  " + "  ".join(f"{t} {100*v:.0f}%" for t, v in sorted(types.items(), key=lambda kv: -kv[1])))
    L.append("")
    foes = {f: sum(r["byFoe"][f] for r in rs) / 2 for f in rs[0]["byFoe"]}
    for f, v in sorted(foes.items(), key=lambda kv: (kv[1], kv[0])):
        L.append(f"{f:<16}{100*v:>5.1f}%")
    return L, foes, types
lb, fb, tb = ladder("d14", "Ironhail / Quarrelstorm, REDESIGNED (sc-ironhail-b14: the hail + sunder, blade 14) win by foe, both sides")
ls, fs, ts = ladder("shipped", "Ironhail as SHIPPED (sc-tendril-t3: the nova, blade 16.23) win by foe, both sides")
cmp_ = ["", "by type, redesign at 14 against shipped:  " + "  ".join(f"{t} {100*tb[t]:.0f}/{100*ts[t]:.0f}" for t in sorted(tb, key=lambda t: -tb[t]))]
text = "\n".join(out) + "\n\n" + "\n".join(lb) + "\n" + "\n".join(cmp_) + "\n\n" + "\n".join(ls) + "\n"
(S / "ladder_b14.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
