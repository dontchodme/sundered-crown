"""v112 §top: THE CARRY AND THE COMPOSE, DRY, on the builder of the day (re-run in the fix round, 2026-09-30).
CARRY: stages 1,2,3,5 on the two newest 02-chain tips. COMPOSE: with the two redesigns built beside it on the same
base (thornwake_build 1,2,3,5; goreshard_build 1,2,5), each before and after this one; the two orders must hold the
same lines. Scratch files, not links.    python carry_compose.py <S> <tmpname>"""
import hashlib, pathlib, re, subprocess, sys
S = pathlib.Path(sys.argv[1]); T = S / "tmp" / sys.argv[2]; T.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path("C:/dev/sundered-crown"); TOOLS = REPO / "tools"; CH = REPO / "02-chain"
PY = sys.executable
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
def nrel(p): return len(re.findall(r'\{ id:"[a-z]+", name:"', pathlib.Path(p).read_text(encoding="utf-8")))
def run(builder, stage, src, out):
    r = subprocess.run([PY, str(TOOLS / builder), "--stage", stage, "--src", str(src), "--out", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(TOOLS))
    if r.returncode or not out.exists():
        raise SystemExit(f"!! {builder} stage {stage} on {src.name}: rc {r.returncode}\n{(r.stdout + r.stderr)[-800:]}")
    return out
HW = ("heartwood_build.py", [("1", "sc-heartwood-stub"), ("2", "sc-heartwood-root"), ("3", "sc-heartwood-rootfast"), ("5", "sc-heartwood-b11")])
OTH = [("thornwake_build.py", [("1", "sc-thornwake-stub"), ("2", "sc-thornwake-bramble"), ("3", "sc-thornwake-snare"), ("5", "sc-thornwake-b26.5")]),
       ("goreshard_build.py", [("1", "sc-goreshard-stub"), ("2", "sc-goreshard-price"), ("5", "sc-goreshard-b10.25")])]
def chain(src, seq, d):
    d.mkdir(parents=True, exist_ok=True); cur = src
    for builder, stages in seq:
        for st, name in stages:
            cur = run(builder, st, cur, d / f"{name}.html")
    return cur
L = [f"CARRY AND COMPOSE, DRY ({sys.argv[2]}): heartwood_build.py {sha(TOOLS / 'heartwood_build.py')}", ""]
for tip in ["sc-spellbreaker-fxout", "sc-aureole-fxout"]:
    src = CH / f"{tip}.html"; d = T / f"carry-{tip}"
    fin = chain(src, [HW], d)
    L.append(f"== CARRY on 02-chain/{tip}.html ({sha(src)}, {nrel(src)} relics): " +
             "  ".join(f"{n} {sha(d / (n + '.html'))}" for _, n in HW[1]) + f"   ({nrel(fin)} relics)")
L.append("")
base = CH / "sc-tendril-t3.html"
for builder, stages in OTH:
    other = (builder, stages)
    a = chain(base, [HW, other], T / f"hw-first-{builder[:-9]}")
    b = chain(base, [other, HW], T / f"{builder[:-9]}-first")
    la = sorted(a.read_text(encoding="utf-8").splitlines()); lb = sorted(b.read_text(encoding="utf-8").splitlines())
    L.append(f"COMPOSE with {builder} ({sha(TOOLS / builder)}) on sc-tendril-t3 ({sha(base)}):")
    L.append(f"  heartwood then {builder[:-9]:<10} -> {a.name:<26} {sha(a)}   ({nrel(a)} relics)")
    L.append(f"  {builder[:-9]:<10} then heartwood -> {b.name:<26} {sha(b)}   ({nrel(b)} relics)")
    L.append("  sorted lines identical: the two orders hold the same lines" if la == lb else "  !! THE TWO ORDERS DIFFER")
text = "\n".join(L) + "\n"; print(text)
(S / "runs" / "carry_compose_fix.txt").write_text(text, encoding="utf-8", newline="\n")
