"""v114 scratch: the §2 gap, four blocks (v99 §4's shape). Side A, the design's 33 foes, 20 seeds a foe,
660 fights an arm a block, seed0 2207 / 2317 / 2427 / 2537. The lab's arm B, the lab at the engine's
window, the lab with fireUlt's cast stop, the built stage-2 link, and the built link with its window on
match time. The blows a cast and the window's blows come from the harness's own columns."""
import json, pathlib, math
R = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard/runs")
B4 = (2207, 2317, 2427, 2537)


def get(prefix, arm, b):
    for p in ([f"{prefix}_{b}.json"] if prefix != "labB" else [f"s0_ASB_{b}.json", f"s0_B_{b}.json"]):
        f = R / p
        if f.exists():
            d = json.load(open(f))["arms"]
            return d.get(arm)
    return None


rows = [("lab B: 8 step-seconds, no cast stop (the design's arm)", "labB", "B"),
        ("lab B with fireUlt's 0.08 cast stop", "ctl_caststop", "B"),
        ("lab B at the engine's window: 8 / (1 - 0.149) = 9.40 s", "ctl_dur940", "B"),
        ("BUILT, the lab's window AND the lab's cast (no 0.08 stop)", "built_matchclock_nostop", "SHIP"),
        ("BUILT, its window on MATCH time (the lab's 8 s)", "built_matchclock", "SHIP"),
        ("BUILT stage 2: 8 s of the window clock", "built_price", "SHIP")]
print(f"  {'':<58} {'2207':>6} {'2317':>6} {'2427':>6} {'2537':>6}   pooled  (n)    blows in / out a fight")
pooled = {}
for name, pre, arm in rows:
    xs = [get(pre, arm, b) for b in B4]
    have = [x for x in xs if x]
    n = sum(x["n"] for x in have)
    w = sum(x["win"] * x["n"] for x in have) / n if n else float("nan")
    hi = sum(x["hitsIn"] * x["n"] for x in have) / n if n else float("nan")
    ho = sum(x["hitsOut"] * x["n"] for x in have) / n if n else float("nan")
    pooled[pre] = (w, n)
    cells = " ".join(f"{100*x['win']:6.1f}" if x else "    --" for x in xs)
    print(f"  {name:<58} {cells}   {100*w:5.1f}  ({n})  {hi:5.2f} / {ho:5.2f}")
se = lambda a, b: 100 * math.sqrt(pooled[a][0] * (1 - pooled[a][0]) / pooled[a][1] + pooled[b][0] * (1 - pooled[b][0]) / pooled[b][1])
print()
for a, b, what in (("built_matchclock_nostop", "labB", "the build on the lab's window and cast, against the lab"),
                   ("built_matchclock", "built_matchclock_nostop", "the build given the cast's 0.08 stop"),
                   ("ctl_dur940", "labB", "the lab's window lengthened to the engine's"),
                   ("ctl_caststop", "labB", "the lab given the cast's 0.08 stop"),
                   ("built_price", "built_matchclock", "the built window: the window clock against match time"),
                   ("built_matchclock", "labB", "the build on the lab's window against the lab"),
                   ("built_price", "labB", "the built relic against the lab (the gap)"),
                   ("built_price", "ctl_dur940", "the built relic against the lab at the engine's window")):
    d = 100 * (pooled[a][0] - pooled[b][0])
    print(f"  {what:<62} {d:+5.1f}  (SE of the difference {se(a, b):.1f}; {d / se(a, b):+.1f} SE)")
