"""v114 scratch: the §4 table -- relic_rate both sides, two blocks, every other
relic a foe (10 seeds a foe a side, 740 fights a block): the shipped relic on
the base, the grid on the stage-2 link (--set dmg=X), the stage-5 link with no
--set (the proof), and the ladder (by type and by foe, 40 fights a foe) at the
final blade, the shipped relic and the design's 9.17."""
import json, pathlib, re, sys
R = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard/runs")
FINAL = sys.argv[1] if len(sys.argv) > 1 else None
ld = lambda f: json.load(open(R / f)) if (R / f).exists() else None


def pair(label):
    return [ld(f"{label}_{b}.json") for b in (2207, 2317)]


def row(name, ds):
    ds = [d for d in ds if d]
    if not ds:
        return None
    g = sum(d["games"] for d in ds)
    w = sum(d["rate"] * d["games"] for d in ds) / g
    wa = sum(d["rateA"] * d["games"] / 2 for d in ds) / (g / 2)
    wb = sum(d["rateB"] * d["games"] / 2 for d in ds) / (g / 2)
    dur = sum(d["dur"] * d["games"] for d in ds) / g
    blocks = "  ".join(f"{100*d['rate']:5.1f}" for d in ds)
    print(f"  {name:<34} {blocks:<14} {100*w:5.1f} ({round(w*g)}/{g})   {100*wa:5.1f}   {100*wb:5.1f}   {dur:5.1f}")
    return w


print("  point                              block 1 / 2    pooled            side A  side B  mean s")
ship = row("SHIPPED: the beam, 9.17 (the base)", pair("ship_rr"))
pts = sorted({float(m.group(1)) for f in R.glob("stage5_rr_d*_2207.json") for m in [re.match(r"stage5_rr_d([\d.]+)_2207", f.name)]})
res = {}
for d in pts:
    lab = f"stage5_rr_d{d:g}"
    res[d] = row(f"the price, blade {d:g}", pair(lab))
if FINAL:
    row(f"BUILT {FINAL} (no --set)", pair("stage5_rr_built"))
if res:
    best = min(res, key=lambda d: abs(res[d] - 0.5))
    print(f"\n  nearest 50% both sides: blade {best:g} ({100*res[best]:.1f}%)")
    if ship is not None:
        near = min(res, key=lambda d: abs(res[d] - ship))
        print(f"  nearest the shipped rate ({100*ship:.1f}%): blade {near:g} ({100*res[near]:.1f}%)")
# THE PROOF: the built link with no --set against the --set run at the same blade, every key
if FINAL:
    blade = re.search(r"b([\d.]+)$", FINAL).group(1)
    for b in (2207, 2317):
        new, ref = ld(f"stage5_rr_built_{b}.json"), ld(f"stage5_rr_d{blade}_{b}.json")
        if not (new and ref):
            continue
        keys = [k for k in sorted(set(new) | set(ref)) if k not in ("game", "set", "label")]
        diff = [k for k in keys if new.get(k) != ref.get(k)]
        print(f"  PROOF block {b}: the stage-5 link with no --set reads {100*new['rate']:.1f}% (A {100*new['rateA']:.1f}, "
              f"B {100*new['rateB']:.1f}), mean {new['dur']:.2f}s; differs from --set dmg={blade} in "
              f"{diff or 'nothing'} ({len(keys)} keys: every foe's rate, byType, both sides, the mean duration)")


def ladder(label, title):
    ds = [d for d in pair(label) if d]
    if len(ds) < 2:
        return
    foes = ds[0]["byFoe"].keys()
    byFoe = {f: sum(d["byFoe"][f] for d in ds) / len(ds) for f in foes}
    types = ds[0]["byType"].keys()
    byType = {t: sum(d["byType"][t] for d in ds) / len(ds) for t in types}
    print(f"\n  LADDER, {title} (40 fights a foe; by type):  " +
          "  ".join(f"{t} {100*v:.0f}" for t, v in sorted(byType.items(), key=lambda kv: -kv[1])))
    srt = sorted(byFoe.items(), key=lambda kv: kv[1])
    print("    by foe, worst first: " + ", ".join(f"{k} {100*v:.1f}" for k, v in srt))


ladder("ship_rr", "the SHIPPED relic (the beam, 9.17)")
ladder("stage5_rr_d9.17", "the price at the design's 9.17")
if FINAL:
    ladder(f"stage5_rr_d{re.search(r'b([\d.]+)$', FINAL).group(1)}", f"the price at the FINAL blade ({FINAL})")
