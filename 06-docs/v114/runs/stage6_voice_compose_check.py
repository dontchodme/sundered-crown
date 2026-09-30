"""SCRATCH. Text-level composition of Goreshard's voice rows (rows_lab.json / rows_final.json) with
(a) Goreshard's picture rows (stage6-picture/rows_final.json), both orders, on the base link and on the
    stage 5 carried onto newer tips (the picture lab's carry/*/sc-goreshard-b10.25.html);
(b) every other relic's stage-6 voice rows whose anchors are on the page, both orders.
Orchestrator semantics: replace = code, after = anchor + code, before = code + anchor; each anchor once.
CONTROL that must fail: my rows applied twice (the second application finds each anchor still once, so the
   check is that the arms are then DOUBLED -- counted) and a row whose anchor is edited out.
usage: compose_check.py <voice rows json>"""
import json, pathlib, sys, itertools
S = pathlib.Path(__file__).resolve().parents[2]          # .../batch
G = S / "goreshard"
mine = json.loads(pathlib.Path(sys.argv[1]).read_bytes().decode("utf-8"))
pic = json.loads((G / "stage6-picture" / "rows_final.json").read_bytes().decode("utf-8"))
pic = pic["rows"] if isinstance(pic, dict) else pic


def one(s, r):
    n = s.count(r["anchor"])
    if n != 1:
        raise ValueError(f"anchor x{n}: {r['label'][:60]}")
    rep = {"replace": r["code"], "after": r["anchor"] + r["code"], "before": r["code"] + r["anchor"]}[r.get("mode", "replace")]
    return s.replace(r["anchor"], rep, 1)


def ap(s, rows):
    for r in rows:
        s = one(s, r)
    return s


pages = {"base b10.25": G / "links" / "sc-goreshard-b10.25.html"}
for d in sorted((G / "stage6-picture" / "carry").iterdir()):
    f = d / "sc-goreshard-b10.25.html"
    if f.exists():
        pages["carry " + d.name] = f
bad = 0
for nm, p in pages.items():
    s = p.read_bytes().decode("utf-8")
    try:
        a = ap(ap(s, mine), pic); b = ap(ap(s, pic), mine)
        ok = a == b
        # each of my codes present once in the result
        k = all(a.count(r["code"]) == 1 for r in mine)
        print(f"  {nm:<34} voice+picture both orders {'IDENTICAL' if ok else 'DIFFER'}; my rows each once: {k}; "
              f"+{len(a) - len(s)} chars")
        bad += (not ok) or (not k)
    except ValueError as e:
        print(f"  {nm:<34} FAILED: {e}"); bad += 1
# (b) other relics' voice rows, on the base
s = pages["base b10.25"].read_bytes().decode("utf-8")
for f in sorted(S.glob("*/stage6-voice/rows_final.json")):
    if f.parent.parent.name == "goreshard":
        continue
    R = json.loads(f.read_bytes().decode("utf-8")); R = R["rows"] if isinstance(R, dict) else R
    R = [r for r in R if s.count(r["anchor"]) == 1]
    if not R:
        continue
    try:
        a = ap(ap(s, mine), R); b = ap(ap(s, R), mine)
        k = all(a.count(r["code"]) == 1 for r in mine) and all(b.count(r["code"]) == 1 for r in mine)
        print(f"  with {f.parent.parent.name:<13} ({len(R)} of its rows on this page): both orders apply; mine each once: {k}; "
              f"results {'identical' if a == b else 'differ only in arm order' if len(a) == len(b) else 'DIFFER IN LENGTH'}")
        bad += (not k) or len(a) != len(b)
    except ValueError as e:
        print(f"  with {f.parent.parent.name:<13} FAILED: {e}"); bad += 1
# CONTROLS
try:
    x = ap(ap(s, mine), mine)
    dbl = sum(x.count(r["code"]) == 2 for r in mine)
    print(f"  CONTROL my rows twice: every anchor still once, and {dbl}/{len(mine)} codes now appear twice "
          f"({'caught, as it must be' if dbl == len(mine) else 'NOT CAUGHT'})")
    bad += dbl != len(mine)
except ValueError as e:
    print(f"  CONTROL my rows twice: refused ({e})")
try:
    ap(s.replace(mine[0]["anchor"], mine[0]["anchor"].replace("kind", "kynd"), 1), mine)
    print("  CONTROL an anchor edited out: APPLIED -- blind"); bad += 1
except ValueError as e:
    print(f"  CONTROL an anchor edited out: refused, as it must be ({e})")
print("EXIT", 1 if bad else 0)
sys.exit(1 if bad else 0)
