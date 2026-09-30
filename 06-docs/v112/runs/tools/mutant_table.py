"""v112 §3: the probe's controls. Each scratch mutant of the final breaks ONE sentence; it must fail the check(s)
named for it and ONLY those, and it must change fights (the probe's own 444 fights: wins, blows in and out of the
windows, casts against the final's -- fight outcomes only, not the tally). m1-m11 are this build's (m8-m10 the
Spellbreaker review's shapes); x1, x2, x4, x5 are the v112 review's (x1/x4/x5 passed the 7-check probe 7/7, the
review's finding 1). x3 (a killing blow roots the dead foe) is printed ASIDE: it decides no fight, so it is not a
control, but it shows which check reads it. The OLD probes are run on the mutants they missed: v1
(tools/heartwood_probe_v1.py) on m8-m10, the 7-check probe (tools/heartwood_probe_v2_c27d9794.py) on x1/x4/x5.
Reads runs/probe_b11.{txt,json}, runs/probe_mut-*.{txt,json}, runs/probev1_mut-*.txt, runs/probe7_mut-*.txt.
    python mutant_table.py <S>"""
import json, pathlib, re, sys
R = pathlib.Path(sys.argv[1]) / "runs"
WANT, ASIDE = {}, {}
for line in (R / "mutants_shas.txt").read_text().splitlines():
    m = re.match(r"(\S+)\s+(want|aside) \[([\d,]+)\]\s+(\w+)", line)
    if m: (WANT if m.group(2) == "want" else ASIDE)[m.group(1)] = ([int(x) for x in m.group(3).split(",")], m.group(4))
def res(tag, pre="probe"):
    t = (R / f"{pre}_{tag}.txt").read_text(encoding="utf-8", errors="replace")
    st = {int(k): v for k, v in re.findall(r"\[(\d)\] (PASS|FAIL)", t)}
    j = json.loads((R / f"{pre}_{tag}.json").read_text()) if (R / f"{pre}_{tag}.json").exists() else None
    return st, j
fst, fj = res("b11")
FS = fj["S"]
def key(S): return (S["wins"], S["bin"], S["bout"], S["casts"])
L = [f"the final sc-heartwood-b11 (--stage 5): {sum(v == 'PASS' for v in fst.values())}/{len(fst)}; wins {FS['wins']}/{FS['fights']}, "
     f"blows in/out {FS['bin']}/{FS['bout']}, casts {FS['casts']}, rooted {FS['rooted']}, extra entangle {FS['ent']}", ""]
allok = True
def row(name, ks, sha, aside=False):
    global allok
    tag = f"mut-{name}"
    if not (R / f"probe_{tag}.json").exists():
        L.append(f"{name:<22} (not run)"); allok &= aside; return
    st, j = res(tag); S = j["S"]
    failed = sorted(c for c, v in st.items() if v == "FAIL")
    nfail = {k: j["n"].get(f"x{k}", 0) for k in failed}
    moved = key(S) != key(FS)
    ok = failed == sorted(ks) and moved
    if not aside: allok &= ok
    old = ""
    for pre, lab in (("probev1", "the v1 probe"), ("probe7", "the 7-check probe")):
        if (R / f"{pre}_{tag}.txt").exists():
            ost, _ = res(tag, pre)
            of = sorted(c for c, v in ost.items() if v == "FAIL")
            old += f"   | {lab}: {'MISSES IT, ' + str(sum(v == 'PASS' for v in ost.values())) + '/' + str(len(ost)) if not of else 'fails ' + str(of)}"
    verdict = ("ASIDE (decides no fight)" if aside and not moved else "ASIDE") if aside else ("OK" if ok else "NOT A CONTROL")
    L.append(f"{name:<22} {sha}  {'reads' if aside else 'want'} {sorted(ks)}  fails {failed} {nfail}  "
             f"wins {S['wins']}/{S['fights']} blows {S['bin']}/{S['bout']} casts {S['casts']}  "
             f"fights {'CHANGED' if moved else 'UNCHANGED'}  -> {verdict}{old}")
    for k in (failed if aside else ks):
        for msg in j["bad"].get(str(k), [])[:1]:
            L.append(f"      [{k}] e.g. {msg[:170]}")
for name, (ks, sha) in WANT.items(): row(name, ks, sha)
if ASIDE:
    L.append("")
    for name, (ks, sha) in ASIDE.items(): row(name, ks, sha, aside=True)
L += ["", "EVERY MUTANT FAILS ITS OWN CHECK(S), ONLY THOSE, AND CHANGES FIGHTS" if allok else "!! NOT EVERY MUTANT IS A CONTROL"]
text = "\n".join(L) + "\n"
(R / "probe_mutants.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
