"""Stage 6's probe counters must not reuse a name [1]-[8] counts. The first extended probe did: [10] counted
"inOk" / "outOk", [2]'s own names, and the fx run's [2] counters came back inflated (837049 / 2671406 against the
b12.5's 418585 / 873316). The test: for every name counted in the stages 1-5 probe, the number of inc(...) sites
that name it must be the same in the stage-6 probe (a stage-6 line may keep an old site, as the close line keeps
clockCloses; it may not add one). Control: the same test on the first extended probe must fail on inOk / outOk."""
import pathlib, re, sys
S = pathlib.Path(__file__).parent
def sites(text):
    c = {}
    for call in re.findall(r"inc\(([^;]*?)\)(?=;|\s*$|\s*}|\s*\n)", text, flags=re.M):
        for q in re.findall(r'"([A-Za-z0-9_]+)"', call):
            c[q] = c.get(q, 0) + 1
    return c
pre = sites((S / "aureole_probe.pre-s6.py").read_text(encoding="utf-8"))
def check(text, tag):
    fin = sites(text)
    bad = {k: (v, fin.get(k, 0)) for k, v in pre.items() if fin.get(k, 0) != v}
    print(f"{tag}: [1]-[8]'s {len(pre)} counter names, sites before/after: " + (f"CHANGED {bad}" if bad else "all unchanged")
          + f"; {len(set(fin) - set(pre))} names new")
    return not bad
fin_t = pathlib.Path("C:/dev/sundered-crown/tools/aureole_probe.py").read_text(encoding="utf-8")
ok = check(fin_t, "the stage-6 probe")
ctl = fin_t.replace('"picInOk" : "picInHeldOk") : "picOutOk"', '"inOk" : "inHeldOk") : "outOk"')
assert ctl != fin_t
cok = check(ctl, "CONTROL (the first extended probe's names put back)")
print("control " + ("PASSES (BAD)" if cok else "fails, as it must"))
sys.exit(0 if ok and not cok else 1)
