"""v112 §6a: the stage-6 probe's controls. The four stage-6 mutants of sc-heartwood-b11-fx (tools/mutants6.py), run
at --stage 6, must fail the check named for each and ONLY that: the two voice mutants ([9]) move no fight -- a voice
decides nothing, which is why the probe has to read it inside the hooks -- and the two picture-hook mutants ([10])
do. Then the fifteen stage 0-5 controls (and x3 aside) re-run at --stage 5 on the stage-6 probe must read as they
did on the fix round's probe (runs/probe_mutants.txt): the same failing checks, the same fights.
Reads runs/stage6_probe/probe_{fx,b11,mut-*}.{txt,json}, runs/mutants_shas.txt, runs/mutants6_shas.txt.
    python mutant_table6.py <S>"""
import json, pathlib, re, sys
S = pathlib.Path(sys.argv[1]); R = S / "runs"; P = R / "stage6_probe"
def res(tag):
    t = (P / f"probe_{tag}.txt").read_text(encoding="utf-8", errors="replace")
    st = {int(k): v for k, v in re.findall(r"\[(\d+)\] (PASS|FAIL)", t)}
    return st, json.loads((P / f"probe_{tag}.json").read_text())
def key(S_): return (S_["wins"], S_["bin"], S_["bout"], S_["casts"])
fst, fj = res("fx"); bst, bj = res("b11")
FS = fj["S"]
L = [f"the stage-6 link sc-heartwood-b11-fx (--stage 6, --no-draw): {sum(v == 'PASS' for v in fst.values())}/{len(fst)}; "
     f"wins {FS['wins']}/{FS['fights']}, blows in/out {FS['bin']}/{FS['bout']}, casts {FS['casts']}, rooted {FS['rooted']}",
     f"the final sc-heartwood-b11 (--stage 5): {sum(v == 'PASS' for v in bst.values())}/{len(bst)}; the same fights "
     f"{'YES' if key(bj['S']) == key(FS) else 'NO'}", ""]
allok = sum(v == "PASS" for v in fst.values()) == 10 and sum(v == "PASS" for v in bst.values()) == 8
SH6 = dict(re.findall(r"mut-(\S+)\.html\s+(\w+)", (R / "mutants6_shas.txt").read_text()))
WANT6 = {"s6-close-voice": ([9], False), "s6-kill-voice": ([9], False), "s6-grove-sim": ([10], True), "s6-grove-rng": ([10], True)}
L.append("STAGE 6's CONTROLS (--stage 6, --no-draw):")
for name, (ks, moves) in WANT6.items():
    st, j = res(f"mut-{name}")
    failed = sorted(c for c, v in st.items() if v == "FAIL")
    moved = key(j["S"]) != key(FS)
    ok = failed == ks and moved == moves
    allok &= ok
    L.append(f"  {name:<16} {SH6.get(name, '?')}  want {ks}  fails {failed} "
             f"{ {k: j['n'].get(f'x{k}', 0) for k in failed} }  fights {'CHANGED' if moved else 'UNCHANGED'} "
             f"(want {'CHANGED' if moves else 'UNCHANGED: a voice decides nothing'})  -> {'OK' if ok else 'NOT A CONTROL'}")
    for k in ks:
        for msg in j["bad"].get(str(k), [])[:1]:
            L.append(f"      [{k}] e.g. {msg[:170]}")
L.append("")
L.append("THE FIFTEEN STAGE 0-5 CONTROLS ON THE STAGE-6 PROBE (--stage 5), against the fix round's table (runs/probe_mutants.txt):")
OLD = {}
for line in (R / "probe_mutants.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(\S+)\s+(\w{16})\s+(want|reads) (\[[\d, ]+\])\s+fails (\[[\d, ]*\]) .*?wins (\d+)/444 blows (\d+)/(\d+) casts (\d+)", line)
    if m: OLD[m.group(1)] = (m.group(3), json.loads(m.group(5)), (int(m.group(6)), int(m.group(7)), int(m.group(8)), int(m.group(9))))
for name, (kind, ofail, okey) in OLD.items():
    if not (P / f"probe_mut-{name}.json").exists():
        L.append(f"  {name:<22} (not run)"); allok = False; continue
    st, j = res(f"mut-{name}")
    failed = sorted(c for c, v in st.items() if v == "FAIL")
    same = failed == ofail and key(j["S"]) == okey
    allok &= same
    L.append(f"  {name:<22} {'reads' if kind == 'reads' else 'want '} fails {failed}  (the fix round's probe: {ofail})  "
             f"fights {'the same' if key(j['S']) == okey else 'DIFFERENT'}  -> {'AS BEFORE' if same else 'CHANGED'}")
L += ["", "EVERY STAGE-6 CONTROL FAILS ITS OWN CHECK AND ONLY IT; EVERY STAGE 0-5 CONTROL READS AS BEFORE" if allok
      else "!! NOT EVERY CONTROL READS AS IT MUST"]
text = "\n".join(L) + "\n"
(R / "stage6_probe_mutants.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
