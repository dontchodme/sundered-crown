"""Scratch (v105 §3): the mutants' table -- each probe's verdicts and its engine_ab count, into one file."""
import pathlib, re, sys
R = pathlib.Path(sys.argv[1])
MUT = [("window", "the window 1% long (dur x 1.01 at the cast)", 1), ("nolead", "no lead: aim at where the foe IS", 2),
       ("cadence", "the stream 10% quicker in the window", 3), ("dmg", "the window's arrows 10% harder", 4),
       ("bladehex", "the second hex on blade blows too", 5), ("nudge", "the aim nudges the caster (vx += 1e-9)", 6),
       ("wait", "the cast waits 0.5 past its charge", 7)]
out = ["MUTANTS of sc-oracle-b10 (variants.py; oracle_probe --seeds 2, 152 fights; engine_ab vs the link, oracle + 7 foes, n=4)", ""]
ok_all = True
for k, what, want in MUT:
    p = (R / f"probe_mut-{k}.txt").read_text(errors="replace")
    e = (R / f"eab_mut-{k}.txt").read_text(errors="replace")
    fails = [int(x) for x in re.findall(r"\[(\d)\] FAIL", p)]
    diff = re.search(r"FAIL\s+every match identical field for field\s+\S+\s+(\d+) differ", e)
    same = re.search(r"PASS\s+every match identical", e)
    nd = diff.group(1) if diff else ("0" if same else "?")
    good = fails == [want] and nd not in ("0", "?")
    ok_all &= good
    out.append(f"[{want}] {what:<48} fails {fails}  engine_ab {nd}/112 differ   {'OK' if good else 'NOT OK'}")
    for line in p.splitlines():
        if "FAIL" in line and "[" in line:
            out.append("      " + line.strip()[:260])
out.append("")
out.append("EVERY MUTANT FAILS ITS OWN CHECK AND ONLY THAT ONE, AND CHANGES FIGHTS" if ok_all else "!! NOT EVERY MUTANT IS A CLEAN CONTROL")
print("\n".join(out))
