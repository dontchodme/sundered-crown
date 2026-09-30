"""THE ROWS: each applies exactly once, in any order, and the page parses.
[1] structure on the base: every anchor occurs exactly once, the anchors' spans are disjoint, and no row's code
    contains any row's anchor (so no row can create or destroy another's anchor).
[2] forward, reverse and 60 seeded random orders: every row finds its anchor exactly once at its turn, and every
    order yields byte-identical output; node --check on it; no rng()/spawnFx/Math.random/ultFx in any row's code.
[3] the stamp: sha256[:16] of the base with ONLY these rows applied (forward order), and rows_final.json re-read
    from disk reproduces it byte for byte; gs-final.html is that page.
[4] carry: Goreshard's stages 1, 2, 5 rebuilt by tools/goreshard_build.py (read-only use, output in scratch)
    on the tips (02-chain/sc-tendril-t3 = the base's own, sc-tendril-fx, and the batch line's later links: the
    newest *-fxout links on disk), then these rows forward and reverse: every anchor once, byte-identical both
    ways, parses, and the same number of chars added as on the base. And with Goreshard's own voice rows, if any
    are on disk (both orders), and with Heartwood's in-flight picture rows (they share drawWeapon and the
    life map's line).
[5] the other in-progress stage-6 rows on disk (every relic's picture and voice rows_final.json): no anchor of
    theirs overlaps one of these unless both rows only INSERT at the same point (that composes: the anchor stays
    once, as [4] shows on the tip that already carries Coldiron's and Ironhail's rows at those points), and no
    code of theirs carries one of these anchors (or the reverse) -- the ways one relic's carry could break
    another's rows.
[6] a CONTROL that must fail: a row whose anchor occurs many times is refused.
writes rows_final.json. usage: lk_order.py"""
import hashlib, json, pathlib, random, sys, subprocess, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import gs_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")

base = P.src_text()
R = P.rows()
out = HERE / "rows_final.json"
out.write_bytes(json.dumps(R, indent=1, ensure_ascii=False).encode("utf-8"))
R2 = json.loads(out.read_bytes().decode("utf-8"))
assert R2 == R, "rows_final.json does not round-trip"
print(f"rows_final.json: {len(R)} rows, {out.stat().st_size} bytes, sha256[:16] of the file "
      f"{hashlib.sha256(out.read_bytes()).hexdigest()[:16]}, round-trips; ascii {out.read_bytes().isascii()}")

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
rng = random.Random(114)
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
print(f"    Math.random count (comments stripped) base {sc(base).count('Math.random')} -> final {sc(fwd).count('Math.random')}")

# [3]
stamp = hashlib.sha256(fwd.encode("utf-8")).hexdigest()[:16]
final = (HERE / "gs-final.html").read_bytes().decode("utf-8")
print(f"[3] STAMP {stamp}  (base {hashlib.sha256(base.encode()).hexdigest()[:16]}; gs-final.html "
      f"{'matches' if final == fwd else 'DIFFERS'}; +{len(fwd) - len(base)} chars)")

# [4]
CAR = HERE / "carry"; CAR.mkdir(exist_ok=True)
B = HERE.parent.parent
V = None
for vp in (B / "goreshard" / "stage6-voice" / "rows_final.json", B / "goreshard" / "stage6-voice" / "rows_lab.json"):
    if vp.exists():
        V = json.loads(vp.read_bytes().decode("utf-8")); VP = vp; break
tips = [("t3", REPO / "02-chain" / "sc-tendril-t3.html"), ("tendril-fx", REPO / "02-chain" / "sc-tendril-fx.html")]
for q in sorted((REPO / "02-chain").glob("sc-*-fxout.html"), key=lambda p: -p.stat().st_mtime)[:6]:
    tips.append((q.stem.replace("sc-", ""), q))
for name, tip in tips:
    if not tip.exists():
        print("[4] (missing)", tip); continue
    d = CAR / name
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src = tip
    ok = True
    for st, nm in (("1", "stub"), ("2", "price"), ("5", "b10.25")):
        o = d / f"sc-goreshard-{nm}.html"
        p = subprocess.run([PY, str(REPO / "tools" / "goreshard_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            print(f"[4] {name} ({tip.name}): goreshard_build stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-300:]}"); ok = False; break
        src = o
    if not ok: continue
    s = src.read_bytes().decode("utf-8")
    same_as_base = s == base
    try:
        a = apply(s, R2); b = apply(s, R2[::-1]); P.syntax_check(a)
        print(f"[4] on {tip.name} ({hashlib.sha256(tip.read_bytes()).hexdigest()[:16]}) + goreshard stages 1,2,5 "
              f"({hashlib.sha256(s.encode()).hexdigest()[:16]}{', = the base' if same_as_base else ''}): every anchor once, "
              f"forward == reverse {a == b}, parses (+{len(a) - len(s)} chars, the same as on the base: {len(a) - len(s) == len(fwd) - len(base)})")
        (d / "picture.html").write_bytes(a.encode("utf-8"))
        if V is not None:
            x = apply(apply(s, V), R2); y = apply(apply(s, R2), V); P.syntax_check(x)
            print(f"    with Goreshard's {len(V)} voice rows ({VP.name}): voice-then-picture == picture-then-voice {x == y}, parses")
        HW = B / "heartwood" / "stage6-picture" / "rows_final.json"
        if HW.exists():
            H = json.loads(HW.read_bytes().decode("utf-8")); H = H["rows"] if isinstance(H, dict) else H
            try:
                x = apply(apply(s, H), R2); y = apply(apply(s, R2), H); P.syntax_check(x)
                print(f"    with Heartwood's {len(H)} picture rows: theirs-then-mine == mine-then-theirs {x == y}, parses")
            except (AssertionError, SystemExit) as e:
                print(f"    with Heartwood's picture rows: {e}")
    except (AssertionError, SystemExit) as e:
        print(f"[4] on {tip.name}: FAILS -- {e}")
if V is None:
    print("[4] Goreshard's voice rows are not on disk yet (goreshard/stage6-voice/rows_final.json or rows_lab.json)")

# [4b] with Heartwood / Rootfast carried first (its stages 1,2,3,5 by tools/heartwood_build.py, then Goreshard's
#      1,2,5): Heartwood's picture rows (they share drawWeapon, the passes and the life map's oathwound line) and
#      these, both orders
HWR = B / "heartwood" / "stage6-picture" / "rows_final.json"
if HWR.exists():
    H = json.loads(HWR.read_bytes().decode("utf-8")); H = H["rows"] if isinstance(H, dict) else H
    for name, tip in [tips[0]] + [t for t in tips if "spellbreaker" in t[0]]:
        d = CAR / ("hw+" + name)
        if d.exists(): shutil.rmtree(d)
        d.mkdir()
        src = tip; ok = True
        for tool, st in (("heartwood_build.py", "1"), ("heartwood_build.py", "2"), ("heartwood_build.py", "3"), ("heartwood_build.py", "5"),
                         ("goreshard_build.py", "1"), ("goreshard_build.py", "2"), ("goreshard_build.py", "5")):
            o = d / f"sc-{tool[:tool.index('_')]}-{st}.html"
            pr = subprocess.run([PY, str(REPO / "tools" / tool), "--stage", st, "--src", str(src), "--out", str(o)],
                                capture_output=True, text=True, cwd=str(REPO / "tools"))
            if pr.returncode != 0 or not o.exists():
                print(f"[4b] {name}: {tool} stage {st} REFUSED/FAILED: {(pr.stdout + pr.stderr).strip()[-300:]}"); ok = False; break
            src = o
        if not ok: continue
        s0 = src.read_bytes().decode("utf-8")
        try:
            x = apply(apply(s0, H), R2); y = apply(apply(s0, R2), H); P.syntax_check(x); P.syntax_check(y)
            print(f"[4b] on {tip.name} + heartwood 1,2,3,5 + goreshard 1,2,5 ({hashlib.sha256(s0.encode()).hexdigest()[:16]}): "
                  f"Heartwood's {len(H)} picture rows then these == these then Heartwood's: {x == y} (the same lines, only the two relics' "
                  f"inserts at a shared point swap places: {sorted(x.splitlines()) == sorted(y.splitlines())}), both parse; "
                  f"the oathwound life entry after both: {x.count('oathwound: 1.5, ')}x, the heartwood entry {x.count('heartwood: 2.2')}x")
        except (AssertionError, SystemExit) as e:
            print(f"[4b] on {tip.name}: FAILS -- {e}")
        for f in d.glob("*.html"):
            if f.name != "sc-goreshard-5.html": f.unlink()
else:
    print("[4b] Heartwood's picture rows are not on disk")

# [5]
mine = [r["anchor"] for r in R2]
seen = 0
for rel in sorted(p.name for p in B.iterdir() if p.is_dir()):
    for kind in ("stage6-picture", "stage6-voice"):
        f = B / rel / kind / "rows_final.json"
        if not f.exists() or (rel == "goreshard" and kind == "stage6-picture"):
            continue
        try:
            X = json.loads(f.read_bytes().decode("utf-8"))
        except Exception as e:
            print(f"[5] {rel}/{kind}: unreadable ({e})"); continue
        X = X["rows"] if isinstance(X, dict) and "rows" in X else X
        seen += 1
        bad, shared = [], []
        for q in X:
            qa, qc = q.get("anchor", ""), q.get("code", "")
            for r in R2:
                a = r["anchor"]
                if qa and qa == a and q.get("mode") != "replace" and r["mode"] != "replace":
                    shared.append(f"{a.strip()[:34]!r} ({q.get('mode')} / mine {r['mode']})")
                elif qa and (qa in a or a in qa):
                    bad.append(f"OVERLAPS anchor {a[:40]!r} ({q.get('mode')} / mine {r['mode']})")
                if a in qc:
                    bad.append(f"their code carries my anchor {a[:40]!r}")
            for r in R2:
                if qa and qa in r["code"]:
                    bad.append(f"my code carries their anchor {qa[:40]!r}")
        print(f"[5] {rel}/{kind} ({len(X)} rows): {'no hazard' if not bad else 'HAZARD: ' + '; '.join(sorted(set(bad)))}"
              + (f"; shares an insertion point, both inserting (composes: the anchor stays once): {', '.join(sorted(set(shared)))}" if shared else ""))
print(f"[5] {seen} other rows files read")

# [6]
try:
    apply(base, [dict(R2[0], anchor="c.fill();")]); print("[6] CONTROL DID NOT BITE")
except AssertionError as e:
    print(f"[6] CONTROL (an anchor that occurs many times) refused: {e}")
