"""Summarise the probe controls after the THIRD v108 review: every mutant of the final
(mutants2.py's ten, mutants3.py's four, mutants4.py's three) and the first review's r3-halfbow, all
under the probe with the step-tied [1], the beat-reading [7] and (new) the hp-rebuilding [4] and the
sunder-target [5]. -> runs/probe_mutants4.txt"""
import pathlib, re, sys, hashlib
S = pathlib.Path(sys.argv[1]); R = S / "runs"
RV = S.parent.parent / "review-ironhail"
def row(name, txt, html):
    t = txt.read_text(encoding="utf-8", errors="replace")
    win = re.search(r"Ironhail win ([\d.]+%)", t); tot = re.search(r"\n  (\d+)/9\n", t)
    fails = re.findall(r"  \[(\d)\] FAIL  .*?   (\d+) FAIL: \[(.*?)(?:, '|\])", t)
    nx = re.findall(r"  \[(\d)\] FAIL  .*NOT EXERCISED", t)
    sha = hashlib.sha256(html.read_bytes()).hexdigest()[:16] if html.exists() else "?"
    f = "; ".join(f"[{k}] {c}: {m[:110]}" for k, c, m in fails) + "".join(f"; [{k}] NOT EXERCISED" for k in nx)
    ex = re.search(r"\nexit (\d+)", t)
    return f"{name:<16} {sha}  {win.group(1) if win else '?':>6}  {tot.group(1) if tot else '?'}/9  exit {ex.group(1) if ex else '?'}  {f or 'NONE'}"
fin = (R / "probe_sunder.txt").read_text(encoding="utf-8", errors="replace")
psha = hashlib.sha256(pathlib.Path("C:/dev/sundered-crown/tools/ironhail_probe.py").read_bytes()).hexdigest()[:16]
out = ["PROBE CONTROLS ON THE FINAL LINK (sc-ironhail-sunder, 1bedab05b9803465) UNDER THE PROBE OF THE THIRD REVIEW",
       f"(ironhail_probe.py sha16 {psha}: [1] counts tickHail calls a step; [7] reads the fatal beat's kind, side, spot and dmg;",
       " [4] requires the call's hurts to be exactly its landings' [foe, dropDmg, caster] and rebuilds every fighter's hp, ward and pool;",
       " [5] requires the call's sunders to be exactly its landings' [foe, sunder, side])",
       f"the final itself: {re.search(r'  (\d+/9)', fin).group(1)}, Ironhail {re.search(r'Ironhail win ([\d.]+%)', fin).group(1)} on the probe's 444 fights",
       "", "mutant           sha16             win    checks  exit  fails (count: first message)"]
for m in ["m1-frozen","m2-cadence","m3-fall","m4-sundermul","m5-missund","m6-stop","m7-nobeat","m8-bowquiet","m8b-halfbow","m9-novakept"]:
    out.append(row(m, R / f"probe_mut2-{m}.txt", S / "tmp" / f"mut2-{m}.html"))
out += ["", "THE SECOND REVIEW'S MUTANTS (tools/mutants3.py; r-double, r-half, r-beatside byte-identical to the reviewer's files):"]
for m in ["r-double","r-half","r-beatside","r-beatspot"]:
    out.append(row(m, R / f"probe_mut3-{m}.txt", S / "tmp" / f"mut3-{m}.html"))
out += ["", "THE THIRD REVIEW'S MUTANTS (tools/mutants4.py; c-caster and c-chip byte-identical to the reviewer's files; c-selfsunder this build's):"]
for m in ["c-caster","c-chip","c-selfsunder"]:
    out.append(row(m, R / f"probe_mut4-{m}.txt", S / "tmp" / f"mut4-{m}.html"))
out += ["", "THE FIRST REVIEW'S r3-halfbow (a mutant of sc-ironhail-b14, the bow at half cadence in the window):",
        row("r3-halfbow", R / "probe_review-r3-halfbow.txt", RV / "tmp" / "mut-r3-halfbow.html")]
(R / "probe_mutants4.txt").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
print("\n".join(out))
