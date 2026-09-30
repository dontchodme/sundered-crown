"""v114 scratch: the builder re-applied on LATER tips carrying other new relics
(the real batch-line tip, the chain's carried redesigns, and the two parallel
builds' scratch links). For each tip: the stages in order, every anchor found
once, the page parsing, and the build's added/removed lines against that tip
compared with the same on the base -- the same lines in the same order.
Scratch output only; no tip is written.

    python compose_check.py <stages, e.g. 1,2 or 1,2,5>
"""
import difflib, hashlib, pathlib, re, subprocess, sys, shutil
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch")
G = W / "goreshard"
T = pathlib.Path(r"C:/dev/sundered-crown/tools"); C = pathlib.Path(r"C:/dev/sundered-crown/02-chain")
BASE = C / "sc-tendril-t3.html"
PY = sys.executable
STAGES = sys.argv[1].split(",") if len(sys.argv) > 1 else ["1", "2"]
sys.path.insert(0, str(T))
import goreshard_build as GB
NAMES = {"1": "sc-goreshard-stub.html", "2": "sc-goreshard-price.html", "5": f"sc-goreshard-b{GB.TUNED['dmg']}.html",
         "6": f"sc-goreshard-b{GB.TUNED['dmg']}-fx.html"}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def build(tip, d):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    src, outs, logs = tip, [], []
    for st in STAGES:
        o = d / NAMES[st]
        r = subprocess.run([PY, "goreshard_build.py", "--stage", st, "--src", str(src), "--out", str(o)],
                           cwd=T, capture_output=True, text=True, encoding="utf-8")
        logs.append(r.stdout + r.stderr)
        if r.returncode:
            raise SystemExit(f"stage {st} on {tip.name} REFUSED:\n{r.stdout}{r.stderr}")
        outs.append(o); src = o
    return outs, "".join(logs)


CLAUSE = "self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : "


def delta(a, b):
    """The added and removed lines. The damage line is the one line another
    build also edits (Angelus inserts its own clause after the tree's), so a
    removed damage line followed by the same line with exactly the price's
    clause inserted after the tree's prefix is written as one token: the edit
    is the clause, whatever else the tip's line carries."""
    A = a.read_text(encoding="utf-8").splitlines(); B = b.read_text(encoding="utf-8").splitlines()
    d = [l for l in difflib.unified_diff(A, B, n=0, lineterm="") if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    out, i = [], 0
    while i < len(d):
        if (d[i].startswith("-    let dmg = (") and i + 1 < len(d) and d[i + 1].startswith("+")
                and d[i + 1][1:].replace(CLAUSE, "", 1) == d[i][1:] and CLAUSE in d[i + 1]):
            out.append("= the damage line, the price's clause inserted after the tree's"); i += 2
        else:
            out.append(d[i]); i += 1
    return out


print(f"v114 compose check: goreshard_build.py (sha16 {sha(T / 'goreshard_build.py')}) stages {'/'.join(STAGES)} "
      f"re-applied on LATER tips (scratch, not the chain)")
print(f"base = {BASE.name} {sha(BASE)}")
ob, _ = build(BASE, G / "compose" / "base")
dB = delta(BASE, ob[-1])
print(f"  on the base: {' / '.join(sha(o) for o in ob)}; +{sum(l[0]=='+' for l in dB)} -{sum(l[0]=='-' for l in dB)} lines; "
      f"== the links in links/: {[sha(o) == sha(G / 'links' / o.name) for o in ob]}")
tips = [("(a) THE BATCH LINE'S TIP now (Spellbreaker carried; 42 relics; read only)", C / "sc-spellbreaker-fxout.html"),
        ("(b) Aureole's carry (Benediction off the beam: NO other relic a beam; read only)", C / "sc-aureole-fxout.html"),
        ("(c) Widowmaker's carry (read only)", C / "sc-widowmaker-fxout.html"),
        ("(d) Bindweed's stage 6 (read only)", C / "sc-tendril-fx.html"),
        ("(e) Heartwood / Rootfast in flight (its scratch final, on sc-tendril-t3)", W / "heartwood" / "links" / "sc-heartwood-b11.html"),
        ("(f) Thornwake / Bramblesnare in flight (its scratch link, on sc-tendril-t3)", W / "thornwake" / "links" / "sc-thornwake-snare.html"),
        ("(g) THE BATCH LINE'S NEWEST TIP, carried while stage 6 was built (Thornwake carried, 2026-09-30 10:53; read only)", C / "sc-thornwake-fxout.html")]
allok = True
for i, (what, tip) in enumerate(tips):
    if not tip.exists():
        print(f"{what}: not on disk, skipped"); continue
    try:
        outs, log = build(tip, G / "compose" / "abcdefg"[i])
    except SystemExit as e:
        allok = False; print(f"{what} -> {tip.name}: {e}"); continue
    d = delta(tip, outs[-1])
    kept = [l for l in log.splitlines() if "beam's generic tail kept" in l][:1]
    rel = [l for l in log.splitlines() if "relics in the roster" in l][-1:]
    same = d == dB
    allok &= same
    print(f"{what} -> {tip.name} {sha(tip)}")
    print(f"    {' / '.join(sha(o) for o in outs)}; every anchor found once; parses; "
          f"+{sum(l[0]=='+' for l in d)} -{sum(l[0]=='-' for l in d)}; the same lines in the same order as on the base: {same}")
    if kept:
        print("    builder: " + kept[0].strip()[:170])
    if rel:
        print("    builder: " + re.sub(r".*; (\d+ relics in the roster)", r"\1", rel[0].strip()))
print(f"\n{'ALL COMPOSE' if allok else 'A TIP DID NOT COMPOSE'}")
sys.exit(0 if allok else 1)
