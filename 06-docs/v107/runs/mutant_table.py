"""The v107 mutant table under the third-round probe (v5): for each scratch mutant of the final link, which checks
fail (and how often), the probe's Lightkeeper win on its 444 fights, and fightdiff's fights changed / wins.
    python mutant_table.py   (reads probe_mut_<m>_v5.txt and fightdiff_mut_<m>.txt beside it)"""
import pathlib, re
R = pathlib.Path(__file__).parent
M = [("m1-window", "the window 10% long on the window clock"),
     ("m2-clock", "the ticker also on frozen steps (the lab's clock)"),
     ("m3-arrows", "the arrow kill zone 4 wider"),
     ("m4-cd", "the cooldown 10% short after a block"),
     ("m5-shove", "the shove 10% strong"),
     ("m6-bank", "a ball block banks 4"),
     ("m7-stop", "a block stops the world 0.05s"),
     ("m8-side", "the shove always outward (the prose read literally)"),
     ("r1-netsplice", "a net arrow spliced, not stuck (reviewer)"),
     ("r2-pinned", "a pinned foe blocked too (reviewer)"),
     ("r3-castcd", "the cast opens with the cooldown running (reviewer)"),
     ("r4-noward", "an arrow's bank skips the ward (reviewer)"),
     ("r5-stun", "a block also stuns the foe 0.3s (reviewer)"),
     ("r6-hex", "a block also lays a Hex on the foe"),
     ("r7-castsunder", "the cast also lays two Sunder on the foe"),
     ("v3-shade", "a block also shoves a Twinshade shade (reviewer)"),
     ("v4-global", "a block writes STATUS.ward.cap = 120 (reviewer)")]
print(f"{'mutant':<14} {'what it breaks':<52} {'fails':<22} {'probe win':<10} {'fights changed':<15} Lightkeeper wins")
allok = True
for m, what in M:
    p = R / f"probe_mut_{m}_v5.txt"
    t = p.read_text(encoding="utf-8") if p.exists() else ""
    fails = re.findall(r"\[(\d)\] FAIL .*?(\d+) FAIL", t)
    notex = re.findall(r"\[(\d)\] FAIL .*NOT EXERCISED", t)
    win = re.search(r"Lightkeeper win ([\d.]+%)", t)
    fd = (R / f"fightdiff_mut_{m}.txt")
    fdt = fd.read_text(encoding="utf-8") if fd.exists() else ""
    g = re.search(r"(\d+)/(\d+) fights differ; Lightkeeper wins (\d+) -> (\d+)", fdt)
    f = ", ".join(f"[{k}] {n}" for k, n in fails) + ("".join(f" [{k}] not exercised" for k in notex))
    ok = len(fails) + len(notex) == 1
    allok &= ok and bool(g) and g.group(1) != "0"
    print(f"{m:<14} {what:<52} {(f + (' only' if ok else '  <-- NOT ALONE')) if t else 'NOT RUN':<22} "
          f"{win.group(1) if win else '-':<10} {(g.group(1) + '/' + g.group(2)) if g else '-':<15} "
          f"{(g.group(3) + ' -> ' + g.group(4)) if g else '-'}   ({p.name})")
print("\nEVERY MUTANT CHANGES FIGHTS AND FAILS ITS OWN CHECK ALONE" if allok else "\nNOT ALL MUTANTS CLEAN (see above)")
