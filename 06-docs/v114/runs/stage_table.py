"""v114 scratch: the §2 table -- stage 0 on 151, the published 141 numbers, the
built links against their lab arms (the same 33 foes, the same seeds, side A),
the controls, and stage 1 against arm A fight for fight (byFoe and blows)."""
import json, pathlib
R = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard/runs")
P = pathlib.Path(r"C:/dev/sundered-crown/06-docs/v81/runs")
ld = lambda f: json.load(open(R / f)) if (R / f).exists() else None
pub = json.load(open(P / "bloodprice_base.json"))["arms"]; p30 = json.load(open(P / "bloodprice_ps30.json"))["arms"]["B"]


def arm(prefix, a):
    out = []
    for b in (2207, 2317):
        d = ld(f"{prefix}_{b}.json")
        out.append(d["arms"][a] if d else None)
    return out


def fmt(xs):
    return " / ".join(f"{100*x['win']:.1f}" if x else "--" for x in xs)


def pooled(xs):
    xs = [x for x in xs if x]
    return sum(x["win"] * x["n"] for x in xs) / sum(x["n"] for x in xs) if xs else float("nan")


A, SH, B = arm("s0_ASB", "A"), arm("s0_ASB", "SHIP"), arm("s0_ASB", "B")
st1, st2 = arm("built_stub", "SHIP"), arm("built_price", "SHIP")
mc, d94 = arm("built_matchclock", "SHIP"), arm("ctl_dur940", "B")
print("                                   lab on 151 (1 / 2)   published 141   BUILT (1 / 2)               pooled")
print(f"A    no ultimate                   {fmt(A):<20} {100*pub['A']['win']:.1f}            stage 1: {fmt(st1):<18} "
      f"{100*pooled(st1):.1f} (lab {100*pooled(A):.1f})")
print(f"SHIP the beam as shipped           {fmt(SH):<20} {100*pub['SHIP']['win']:.1f}")
print(f"B    the price, perStack 0.30      {fmt(B):<20} {100*p30['win']:.1f}            stage 2: {fmt(st2):<18} "
      f"{100*pooled(st2):.1f} (lab {100*pooled(B):.1f})")
print()
print("controls (blocks 2207 / 2317, side A, 660 fights an arm a block):")
print(f"  lab B: 8 step-seconds (the design's)                      {fmt(B):<14} pooled {100*pooled(B):.1f}")
print(f"  lab B at the engine's window: 8 / (1 - 0.149) = 9.40 s     {fmt(d94):<14} pooled {100*pooled(d94):.1f}")
print(f"  BUILT, its window on MATCH time (the lab's 8 s)           {fmt(mc):<14} pooled {100*pooled(mc):.1f}")
print(f"  BUILT stage 2: 8 s of the window clock                    {fmt(st2):<14} pooled {100*pooled(st2):.1f}")
print()
for lab, blt, name in ((A, st1, "stage 1 vs arm A"), (B, st2, "stage 2 vs arm B")):
    for b, x, y in zip((2207, 2317), lab, blt):
        if not (x and y):
            continue
        same = x["byFoe"] == y["byFoe"]
        print(f"{name} block {b}: win {100*x['win']:.1f} vs {100*y['win']:.1f}; every foe's rate identical: {same}; "
              f"blows a fight (lab in+out {x['hitsIn'] + x['hitsOut']:.4f}, built {y['hitsIn'] + y['hitsOut']:.4f}): "
              f"{abs(x['hitsIn'] + x['hitsOut'] - y['hitsIn'] - y['hitsOut']) < 1e-9}")
