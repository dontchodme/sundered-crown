"""THE ROWS: each applies exactly once, in any order, and the page parses.
[1] structure on the base: every anchor occurs exactly once, the anchors' spans are disjoint, and no row's code
    contains any row's anchor (so no row can create or destroy another's anchor).
[2] forward, reverse and 60 seeded random orders: every row finds its anchor exactly once at its turn, and every
    order yields byte-identical output; node --check on it.
[3] the stamp: sha256[:16] of the base with ONLY these rows applied (forward order), and rows_final.json re-read
    from disk reproduces it byte for byte; sb-final.html is that page.
[4] carry: Spellbreaker's stages 1, 2, 3, 5 rebuilt by tools/spellbreaker_build.py (read-only use, output in
    scratch) on the base's own tip (02-chain/sc-tendril-t3.html) and on the batch line's newer links in 02-chain
    (the tip of the day is sc-aureole-fxout, which carries Aureole's picture rows); then these rows forward and
    reverse: every anchor once, byte-identical both ways, parses, the same number of chars added as on the base;
    SPECS.spellbreaker's exact text present once in each inlined copy (the orchestrator's cut). With Spellbreaker's
    own voice rows (stage6-voice/rows_final.json), both orders.
[5] a CONTROL that must fail: a row whose anchor occurs many times is refused.
writes rows_final.json. usage: order.py"""
import hashlib, json, pathlib, random, sys, subprocess, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import sb_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")

base = P.src_text()
R = P.rows()
out = HERE / "rows_final.json"
out.write_bytes(json.dumps(R, indent=1, ensure_ascii=False).encode("utf-8"))
R2 = json.loads(out.read_bytes().decode("utf-8"))
assert R2 == R, "rows_final.json does not round-trip"
print(f"rows_final.json: {len(R)} rows, {out.stat().st_size} bytes, sha256[:16] of the file "
      f"{hashlib.sha256(out.read_bytes()).hexdigest()[:16]}, round-trips")

# [1]
spans = []
for r in R:
    n = base.count(r["anchor"]); assert n == 1, (r["label"], n)
    i = base.index(r["anchor"]); spans.append((i, i + len(r["anchor"]), r["label"]))
spans.sort()
for (a0, a1, la), (b0, b1, lb) in zip(spans, spans[1:]):
    assert a1 <= b0, ("overlap", la, lb)
for r in R:
    for q in R:
        assert q["anchor"] not in r["code"], ("code carries an anchor", r["label"], q["label"])
print(f"[1] {len(R)} anchors, each once in the base; spans disjoint; no code carries an anchor")


def apply(src, rows):
    for r in rows:
        n = src.count(r["anchor"])
        if n != 1:
            raise AssertionError(f"{r['label']}: anchor found {n}x")
        src = P.one(src, r["anchor"], r["code"], r["mode"], r["label"])
    return src


# [2]
fwd = apply(base, R2)
orders = [list(range(len(R)))[::-1]]
rng = random.Random(79)
for _ in range(60):
    o = list(range(len(R))); rng.shuffle(o); orders.append(o)
for o in orders:
    assert apply(base, [R2[i] for i in o]) == fwd, o
print(f"[2] forward, reverse and 60 random orders: byte-identical ({len(orders) + 1} orders)")
nblk = P.syntax_check(fwd)
print(f"    node --check: {nblk} inline script block(s) parse")
sc = P.strip_comments
for bad in ("rng()", "spawnFx", "Math.random", "ultFx"):
    hits = [r["label"] for r in R2 if bad in sc(r["code"])]
    print(f"    '{bad}' in any row's code (comments stripped): {hits or 'none'}")
print(f"    Math.random count (comments stripped) base {sc(base).count('Math.random')} -> final {sc(fwd).count('Math.random')} (the bolt's flicker retired)")
print(f"    the page after: 'spellbreaker: 1.4' {fwd.count('spellbreaker: 1.4')}x, 'spellbreaker:1,' {fwd.count('spellbreaker:1,')}x, "
      f"'u.w === \"spellbreaker\"' {fwd.count(chr(34).join(['u.w === ', 'spellbreaker', '']))}x, "
      f"'spellbreaker(c, t, cf, P)' {fwd.count('spellbreaker(c, t, cf, P)')}x (the charge rune, kept), "
      f"'b.w === \"spellbreaker\"' {fwd.count(chr(34).join(['b.w === ', 'spellbreaker', '']))}x (the banner scatter, kept), "
      f"SPECS.spellbreaker text {fwd.count(P.FX_OLD)}x (the orchestrator's)")

# [3]
stamp = hashlib.sha256(fwd.encode("utf-8")).hexdigest()[:16]
final = (HERE / "sb-final.html").read_bytes().decode("utf-8")
print(f"[3] STAMP {stamp}  (base {hashlib.sha256(base.encode()).hexdigest()[:16]}; sb-final.html "
      f"{'matches' if final == fwd else 'DIFFERS'}; +{len(fwd) - len(base)} chars)")

# [4]
CAR = HERE / "carry"; CAR.mkdir(exist_ok=True)
B = HERE.parent.parent
VP = HERE.parent / "stage6-voice" / "rows_final.json"
V = json.loads(VP.read_bytes().decode("utf-8")) if VP.exists() else None
tips = [("t3", REPO / "02-chain" / "sc-tendril-t3.html")]
for t in ("sc-aureole-fxout", "sc-aureole-b12.5-fx", "sc-censer-fxout", "sc-censer-consecration-b25.5-fx", "sc-lightkeeper-fxout",
          "sc-angelus-b9-fx", "sc-oracle-fx", "sc-widowmaker-fxout", "sc-lodestone-b205-fx", "sc-ironhail-fxout", "sc-coldiron-temper-fx"):
    if (REPO / "02-chain" / f"{t}.html").exists(): tips.append((t, REPO / "02-chain" / f"{t}.html"))
if V is not None:
    vb = apply(apply(base, V), R2); vc = apply(apply(base, R2), V); P.syntax_check(vb)
    print(f"[4] on the base with the {len(V)} voice rows ({hashlib.sha256(VP.read_bytes()).hexdigest()[:16]}): voice-then-picture == "
          f"picture-then-voice {vb == vc}, parses, sha {hashlib.sha256(vb.encode()).hexdigest()[:16]}")
nok = 0
for name, tip in tips:
    d = CAR / name
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src = tip
    ok = True
    for st in "1235":
        o = d / f"sc-spellbreaker-carry-s{st}.html"
        p = subprocess.run([PY, str(REPO / "tools" / "spellbreaker_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            print(f"[4] {name}: spellbreaker_build stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-300:]}"); ok = False; break
        src = o
    if not ok: continue
    s = src.read_bytes().decode("utf-8")
    same_as_base = s == base
    try:
        a = apply(s, R2); b = apply(s, R2[::-1]); P.syntax_check(a)
        nok += 1
        print(f"[4] on {tip.name} ({hashlib.sha256(tip.read_bytes()).hexdigest()[:16]}) + spellbreaker stages 1-5 "
              f"({hashlib.sha256(s.encode()).hexdigest()[:16]}{', = the base' if same_as_base else ''}): every anchor once, "
              f"forward == reverse {a == b}, parses (+{len(a) - len(s)} chars, the same as on the base: {len(a) - len(s) == len(fwd) - len(base)}); "
              f"SPECS.spellbreaker text {a.count(P.FX_OLD)}x")
        if V is not None:
            x = apply(apply(s, V), R2); y = apply(apply(s, R2), V); P.syntax_check(x)
            print(f"    with the voice's {len(V)} rows: voice-then-picture == picture-then-voice {x == y}, parses")
    except (AssertionError, SystemExit) as e:
        print(f"[4] on {tip.name}: FAILS -- {e}")
    for f in d.glob("*.html"):
        f.unlink()
print(f"[4] {nok} of {len(tips)} carries clean")

# [5]
try:
    apply(base, [dict(R2[0], anchor="c.fill();")]); print("[5] CONTROL DID NOT BITE")
except AssertionError as e:
    print(f"[5] CONTROL (an anchor that occurs many times) refused: {e}")
