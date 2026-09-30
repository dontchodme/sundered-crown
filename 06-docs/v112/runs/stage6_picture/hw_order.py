"""THE ROWS: each applies exactly once, in any order, and the page parses.
[1] structure on the base: every anchor occurs exactly once, the anchors' spans are disjoint, and no row's code
    contains any row's anchor (so no row can create or destroy another's anchor).
[2] forward, reverse and 60 seeded random orders: every row finds its anchor exactly once at its turn, and every
    order yields byte-identical output; node --check on it; the forbidden tokens.
[3] the stamp: sha256[:16] of the base with ONLY these rows applied (forward order), and rows_final.json re-read
    from disk reproduces it byte for byte; hw-final.html is that page.
[4] carry: Heartwood's stages 1,2,3,5 rebuilt by tools/heartwood_build.py (read-only use, output in scratch) on the
    real tips (02-chain/sc-tendril-t3 = the base's own, sc-tendril-fx = the first with Tendril's root, and
    sc-spellbreaker-fxout = the newest) and on the other scratch pictures on disk built beside this one, then these
    rows forward and reverse: every anchor once, byte-identical both ways, parses, the same chars added as on the
    base; on a tip that carries Tendril's picture, its root and guard are present for the markers to drive.
    And with Heartwood's own voice rows, if any are on disk (both orders).
[5] a CONTROL that must fail: a row whose anchor occurs many times is refused.
writes rows_final.json. usage: hw_order.py"""
import hashlib, json, pathlib, random, sys, subprocess, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import hw_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]

base = P.src_text()
R = P.rows(base)
out = HERE / "rows_final.json"
out.write_bytes(json.dumps(R, indent=1, ensure_ascii=False).encode("utf-8"))
R2 = json.loads(out.read_bytes().decode("utf-8"))
assert R2 == R, "rows_final.json does not round-trip"
print(f"rows_final.json: {len(R)} rows, {out.stat().st_size} bytes, sha256[:16] of the file {sha(out.read_bytes())}, round-trips")

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
rng = random.Random(112)
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
stamp = sha(fwd)
final = (HERE / "hw-final.html").read_bytes().decode("utf-8")
print(f"[3] STAMP {stamp}  (base {sha(base)}; hw-final.html {'matches' if final == fwd else 'DIFFERS'}; +{len(fwd) - len(base)} chars)")

# [4]
CAR = HERE / "carry"; CAR.mkdir(exist_ok=True)
B = HERE.parent.parent
V = None
for vp in (B / "heartwood" / "stage6-voice" / "rows_final.json", B / "heartwood" / "stage6-voice" / "rows_lab.json"):
    if vp.exists():
        V = json.loads(vp.read_bytes().decode("utf-8")); VP = vp; break
tips = [("t3", REPO / "02-chain" / "sc-tendril-t3.html"), ("tendril-fx", REPO / "02-chain" / "sc-tendril-fx.html"),
        ("spellbreaker-fxout", REPO / "02-chain" / "sc-spellbreaker-fxout.html")]
for rel, fn in (("ironhail", "ih-final.html"), ("coldiron", "ci-final.html"), ("censer", "ce-final.html"),
                ("lightkeeper", "lk-final.html"), ("widowmaker", "wm-final.html"), ("lodestone", "ld-final.html"),
                ("oracle", "or-final.html"), ("spellbreaker", "sb-final.html"), ("aureole", "au-final.html"),
                ("angelus", "an-final.html"), ("bindweed", "bw-final.html"), ("portcullis", "pc-final.html")):
    p = B / rel / "stage6-picture" / fn
    if p.exists(): tips.append((rel, p))
for name, tip in tips:
    d = CAR / f"ord-{name}"
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src = tip; ok = True
    for st, nm in (("1", "stub"), ("2", "root"), ("3", "rootfast"), ("5", "b11")):
        o = d / f"sc-heartwood-{nm}.html"
        p = subprocess.run([PY, str(REPO / "tools" / "heartwood_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            print(f"[4] {name} ({tip.name}): heartwood_build stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-300:]}"); ok = False; break
        src = o
    if not ok:
        shutil.rmtree(d); continue
    s = src.read_bytes().decode("utf-8")
    try:
        a = apply(s, R2); b = apply(s, R2[::-1]); P.syntax_check(a)
        tw = all(t in s for t in ("if (f.twineHeld && !(f.pin > 0 && f.alive)) f.twineHeld = 0;",
                                  "!(f.twineHeld > 0)){", "_twineRoot(m, f, 0)", "_twineRoot(m, f, 1)"))
        print(f"[4] on {tip.name} ({sha(tip.read_bytes())}) + heartwood 1,2,3,5 ({sha(s)}{', = the base' if s == base else ''}): "
              f"every anchor once, forward == reverse {a == b}, parses (+{len(a) - len(s)} chars, as on the base: "
              f"{len(a) - len(s) == len(fwd) - len(base)}); Tendril's root + guard on it: {tw}")
        if V is not None:
            x = apply(apply(s, V), R2); y = apply(apply(s, R2), V); P.syntax_check(x)
            print(f"    with Heartwood's {len(V)} voice rows ({VP.name}): voice-then-picture == picture-then-voice {x == y}, parses")
    except (AssertionError, SystemExit) as e:
        print(f"[4] on {tip.name}: FAILS -- {e}")
    shutil.rmtree(d)
if V is None:
    print("[4] Heartwood's voice rows are not on disk yet (heartwood/stage6-voice/rows_final.json or rows_lab.json)")

# [5]
try:
    apply(base, [dict(R2[0], anchor="c.fill();")]); print("[5] CONTROL DID NOT BITE")
except AssertionError as e:
    print(f"[5] CONTROL (an anchor that occurs many times) refused: {e}")
