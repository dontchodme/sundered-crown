"""THE ROWS: each applies exactly once, in any order, and the page parses.
[1] structure on the base: every anchor occurs exactly once, the anchors' spans are disjoint, and no row's code
    contains any row's anchor (so no row can create or destroy another's anchor).
[2] forward, reverse and 60 seeded random orders: every row finds its anchor exactly once at its turn, and every
    order yields byte-identical output; node --check on it.
[3] the stamp: sha256[:16] of the base with ONLY these rows applied (forward order), and rows_final.json re-read
    from disk reproduces it byte for byte; ld-final.html is that page.
[4] carry: Lodestone's stages 1,2,3,5 rebuilt by tools/lodestone_build.py (read-only use, output in scratch) on
    the real tip (02-chain/sc-tendril-fx.html, Bindweed's picture) and on the other stage-6 pictures on disk
    (Coldiron's ci-final, Ironhail's ih-final-fx, Portcullis's pc-final), plus the composed links the round-3
    compose test left (Lodestone on seven other builds' links), then these rows forward and reverse: every
    anchor once, byte-identical both ways, parses, and the same number of chars added as on the base. And with
    Lodestone's own voice rows, if any are on disk (both orders).
[5] a CONTROL that must fail: a row whose anchor occurs many times is refused.
writes rows_final.json. usage: ld_order.py"""
import hashlib, json, pathlib, random, sys, subprocess, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import ld_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")
B = HERE.parent.parent

base = P.src_text()
R = P.rows()
out = HERE / "rows_final.json"
out.write_bytes(json.dumps(R, indent=1, ensure_ascii=False).encode("utf-8"))
R2 = json.loads(out.read_bytes().decode("utf-8"))
assert R2 == R, "rows_final.json does not round-trip"
print(f"rows_final.json: {len(R)} rows, {out.stat().st_size} bytes, sha256[:16] of the file "
      f"{hashlib.sha256(out.read_bytes()).hexdigest()[:16]}, round-trips; all ASCII: {out.read_bytes().isascii()}")

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
rng = random.Random(102)
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
final = (HERE / "ld-final.html").read_bytes().decode("utf-8")
print(f"[3] STAMP {stamp}  (base {hashlib.sha256(base.encode()).hexdigest()[:16]}; ld-final.html "
      f"{'matches' if final == fwd else 'DIFFERS'}; +{len(fwd) - len(base)} chars)")

# [4]
CAR = HERE / "carry"; CAR.mkdir(exist_ok=True)
V = None
for vp in (B / "lodestone" / "stage6-voice" / "rows_final.json", B / "lodestone" / "stage6-voice" / "rows_lab.json"):
    if vp.exists():
        V = json.loads(vp.read_bytes().decode("utf-8")); VP = vp; break
if V is None:
    cands = sorted((B / "lodestone" / "stage6-voice").glob("rows_lab*.json"), key=lambda p: p.stat().st_mtime)
    if cands:
        VP = cands[-1]; V = json.loads(VP.read_bytes().decode("utf-8"))
tips = [("tip", REPO / "02-chain" / "sc-tendril-fx.html"),
        ("coldiron", B / "coldiron" / "stage6-picture" / "ci-final.html"),
        ("ironhail", B / "ironhail" / "stage6-picture" / "ih-final-fx.html"),
        ("portcullis", B / "portcullis" / "stage6-picture" / "pc-final.html")]
done = []
for name, tip in tips:
    if not tip.exists():
        print("[4] (missing)", tip); continue
    d = CAR / name
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src = tip
    ok = True
    for st in "1235":
        o = d / f"sc-lodestone-carry-s{st}.html"
        p = subprocess.run([PY, str(REPO / "tools" / "lodestone_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            print(f"[4] {name} ({tip.name}): lodestone_build stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-300:]}"); ok = False; break
        src = o
    if ok: done.append((f"{tip.name} + lodestone 1,2,3,5", tip, src))
for c in sorted((B / "lodestone" / "ctl" / "compose205").glob("*-5.html")):
    if c.name.startswith("sc-tendril-fx"): continue
    done.append((f"{c.name} (round-3 compose)", c, c))
for label, tip, src in done:
    s = src.read_bytes().decode("utf-8")
    same_as_base = s == base
    try:
        a = apply(s, R2); b = apply(s, R2[::-1]); P.syntax_check(a)
        print(f"[4] on {label} ({hashlib.sha256(s.encode()).hexdigest()[:16]}{', = the base' if same_as_base else ''}): every anchor once, "
              f"forward == reverse {a == b}, parses (+{len(a) - len(s)} chars, the same as on the base: {len(a) - len(s) == len(fwd) - len(base)})")
        if V is not None:
            x = apply(apply(s, V), R2); y = apply(apply(s, R2), V); P.syntax_check(x)
            print(f"    with Lodestone's {len(V)} voice rows ({VP.name}): voice-then-picture == picture-then-voice {x == y}, parses")
    except (AssertionError, SystemExit) as e:
        print(f"[4] on {label}: FAILS -- {e}")
if V is None:
    print("[4] Lodestone's voice rows are not on disk yet (lodestone/stage6-voice/rows_final.json)")

# [5]
try:
    apply(base, [dict(R2[0], anchor="c.fill();")]); print("[5] CONTROL DID NOT BITE")
except AssertionError as e:
    print(f"[5] CONTROL (an anchor that occurs many times) refused: {e}")
