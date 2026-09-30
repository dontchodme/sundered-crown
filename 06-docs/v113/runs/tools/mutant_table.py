"""v113 §3: the probe's controls. Each scratch mutant of the final breaks ONE sentence; it must fail the check(s)
named for it and ONLY those, and it must change fights (the probe's own 444: wins, blows in/out, casts, brambles,
bites, snares against the final's) -- m11 excepted and said (a beat is the director's; it cannot change a fight).
Reads runs/probe_final.{txt,json}, runs/probe_mut-*.{txt,json}, runs/mutants_shas.txt.
    python mutant_table.py <S>"""
import json, pathlib, re, sys
R = pathlib.Path(sys.argv[1]) / "runs"
WANT = {}
for line in (R / "mutants_shas.txt").read_text().splitlines():
    m = re.match(r"(\S+)\s+want \[([\d,]+)\]\s+(\w+)", line)
    if m: WANT[m.group(1)] = ([int(x) for x in m.group(2).split(",")], m.group(3))
def res(tag):
    t = (R / f"probe_{tag}.txt").read_text(encoding="utf-8", errors="replace")
    st = {int(k): v for k, v in re.findall(r"\[(\d)\] (PASS|FAIL)", t)}
    j = json.loads((R / f"probe_{tag}.json").read_text()) if (R / f"probe_{tag}.json").exists() else None
    return st, j
fst, fj = res("final")
FS = fj["S"]
def key(S): return (S["wins"], S["bin"], S["bout"], S["casts"], S["planted"], S["ticks"], S["snares"])
L = [f"the final (--stage 5): {sum(v == 'PASS' for v in fst.values())}/{len(fst)}; wins {FS['wins']}/{FS['fights']}, "
     f"blows in/out {FS['bin']}/{FS['bout']}, casts {FS['casts']}, brambles {FS['planted']}, bites {FS['ticks']}, snares {FS['snares']}", ""]
allok = True
for name, (ks, sha) in WANT.items():
    tag = f"mut-{name}"
    if not (R / f"probe_{tag}.json").exists():
        L.append(f"{name:<24} (not run)"); allok = False; continue
    st, j = res(tag); S = j["S"]
    failed = sorted(c for c, v in st.items() if v == "FAIL")
    nfail = {k: j["n"].get(f"x{k}", 0) for k in failed}
    moved = key(S) != key(FS)
    beat_only = name.startswith("m11")
    ok = failed == sorted(ks) and (moved or beat_only)
    allok &= ok
    L.append(f"{name:<24} {sha}  want {sorted(ks)}  fails {failed} {nfail}  "
             f"wins {S['wins']}/{S['fights']} blows {S['bin']}/{S['bout']} casts {S['casts']} brambles {S['planted']} bites {S['ticks']} snares {S['snares']}  "
             f"fights {'CHANGED' if moved else 'UNCHANGED' + (' (a beat cannot change a fight)' if beat_only else '')}  -> {'OK' if ok else 'NOT A CONTROL'}")
    for k in ks:
        for msg in j["bad"].get(str(k), [])[:1]:
            L.append(f"      [{k}] e.g. {msg[:170]}")
L += ["", "EVERY MUTANT FAILS ITS OWN CHECK(S), ONLY THOSE, AND CHANGES FIGHTS (m11 aside, a beat)" if allok else "!! NOT EVERY MUTANT IS A CONTROL"]
text = "\n".join(L) + "\n"
(R / "probe_mutants.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
