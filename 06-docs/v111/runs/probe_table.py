"""v111 §3's results table from the probe's own txt files (one row a link)."""
import re, sys
S = sys.argv[1]
rows = [("sc-spellbreaker-stun", "stun", "2"), ("sc-spellbreaker-unmaking", "unm", "3"), ("sc-spellbreaker-b7.5", "b7.5", "5 (the final)"),
        ("sc-spellbreaker-b8.3", "b8.3", "5 --alt-row"), ("sc-spellbreaker-b7.7", "b7.7", "5 --alt50")]
print(f"{'link':<26} {'stage':<14} checks  casts  blows in / out   blows a cast  2nd hex a cast  hex a live blow  foe hex/frame  foe stunned in / out   cadence calls  window (match)  frozen  win (444)")
for name, tag, st in rows:
    t = open(f"{S}/probe_{tag}.txt", encoding="utf-8").read()
    g = lambda p: re.search(p, t)
    cf = g(r"casts/fight ([\d.]+)   blows a fight: in windows ([\d.]+), outside ([\d.]+)   Spellbreaker win ([\d.]+)%")
    pc = g(r"unmade \(blows in the window\) ([\d.]+)   hex \(the second hex\) ([\d.]+)   hex applied by her blows in windows on a live body / those blows ([\d.]+)")
    fh = g(r"hex stacks ([\d.]+)   its weapon stunned ([\d.]+)% of window frames \(outside windows ([\d.]+)%\)")
    cad = g(r"the cadence: (\d+) tickStatus calls")
    fr = g(r"FREEZE CENSUS ([\d.]+)% of window steps frozen   a clock window lasts ([\d.]+)s")
    ok = g(r"\n  (\d)/6")
    print(f"{name:<26} {st:<14} {ok.group(1)}/6     {cf.group(1)}   {cf.group(2)} / {cf.group(3)}    {pc.group(1):<12}  {pc.group(2):<14}  {pc.group(3):<15}  {fh.group(1):<13}  {fh.group(2)}% / {fh.group(3)}%          {cad.group(1):<13}  {fr.group(2)}s           {fr.group(1)}%   {cf.group(4)}%")
