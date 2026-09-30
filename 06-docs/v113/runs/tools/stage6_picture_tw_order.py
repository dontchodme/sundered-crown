"""THE ROWS: each applies exactly once, in any order, and the page parses.
[1] structure on the base: every anchor occurs exactly once, the anchors' spans are disjoint, and no row's code
    contains any row's anchor (so no row can create or destroy another's anchor).
[2] forward, reverse and 60 seeded random orders: every row finds its anchor exactly once at its turn, and every
    order yields byte-identical output; node --check on it.
[3] the stamp: sha256[:16] of the base with ONLY these rows applied (forward order), and rows_final.json re-read
    from disk reproduces it byte for byte; tw-final.html is that page.
[4] carry: Thornwake's stages 1, 2, 3, 5 rebuilt by tools/thornwake_build.py (read-only use, output in scratch) on the
    real base tip (02-chain/sc-tendril-t3.html), on sc-tendril-fx (Tendril's picture: the root picture the snare
    reuses, and its hexagon guard), on the batch line's newer links in 02-chain, and on the other scratch pictures on
    disk; then these rows forward and reverse: every anchor once, byte-identical both ways, parses, and the same
    number of chars added as on the base; SPECS.thornwake's exact text (with its FREEZE comment) present once in each
    inlined copy (the orchestrator's cut). With Thornwake's own voice rows (stage6-voice/rows_final.json, if on disk)
    and with Heartwood's picture rows (the other freeze redesign; heartwood_build.py stages 1, 2, 3, 5 first), both
    orders.
[5] a CONTROL that must fail: a row whose anchor occurs many times is refused.
writes rows_final.json. usage: tw_order.py"""
import hashlib, json, pathlib, random, sys, subprocess, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import idle  # noqa
import tw_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]

base = P.src_text()
R = P.rows()
out = HERE / "rows_final.json"
out.write_bytes(json.dumps(R, indent=1, ensure_ascii=False).encode("utf-8"))
R2 = json.loads(out.read_bytes().decode("utf-8"))
assert R2 == R, "rows_final.json does not round-trip"
print(f"rows_final.json: {len(R)} rows, {out.stat().st_size} bytes, sha256[:16] of the file {sha(out.read_bytes())}, "
      f"round-trips; ASCII: {all(r['code'].isascii() and r['anchor'].isascii() for r in R)}")

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
rng = random.Random(84)
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
print(f"    the page after: 'thornwake: 2.4' {fwd.count('thornwake: 2.4')}x, 'thornwake:1' {fwd.count('thornwake:1')}x, "
      f"'u.w === \"thornwake\"' {fwd.count(chr(34).join(['u.w === ', 'thornwake', '']))}x, "
      f"ULTSIG 'thornwake(c, t, cf, P)' {fwd.count('thornwake(c, t, cf, P)')}x, banner 'b.w === \"thornwake\"' "
      f"{fwd.count(chr(34).join(['b.w === ', 'thornwake', '']))}x, SPECS.thornwake block {fwd.count(P.FX_BLOCK)}x (the orchestrator's)")

# [3]
stamp = sha(fwd)
final = (HERE / "tw-final.html").read_bytes().decode("utf-8")
print(f"[3] STAMP {stamp}  (base {sha(base)}; tw-final.html {'matches' if final == fwd else 'DIFFERS'}; +{len(fwd) - len(base)} chars)")

# [4]
CAR = HERE / "carry"; CAR.mkdir(exist_ok=True)
B = HERE.parent.parent
V = None
VP = B / "thornwake" / "stage6-voice" / "rows_final.json"
if VP.exists():
    V = json.loads(VP.read_bytes().decode("utf-8"))
    x = apply(apply(base, V), R2); y = apply(apply(base, R2), V); P.syntax_check(x)
    print(f"[4] on the base with Thornwake's {len(V)} voice rows ({VP.name}, {sha(VP.read_bytes())}): "
          f"voice-then-picture == picture-then-voice {x == y}, parses, {sha(x)}")
else:
    print("[4] Thornwake's voice rows are not on disk yet (thornwake/stage6-voice/rows_final.json)")
HWP = B / "heartwood" / "stage6-picture" / "rows_final.json"
HW = json.loads(HWP.read_bytes().decode("utf-8")) if HWP.exists() else None


def build_stages(tip, d, builder, prefix):
    src = tip
    for st in "1235":
        o = d / f"{prefix}-s{st}.html"
        p = subprocess.run([PY, str(REPO / "tools" / builder), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            return None, f"{builder} stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-300:]}"
        src = o
    return src, None


tips = [("tip", REPO / "02-chain" / "sc-tendril-t3.html"),
        ("tendril-fx", REPO / "02-chain" / "sc-tendril-fx.html"),
        ("spellbreaker-fxout", REPO / "02-chain" / "sc-spellbreaker-fxout.html"),
        ("aureole-fxout", REPO / "02-chain" / "sc-aureole-fxout.html"),
        ("ironhail-fxout", REPO / "02-chain" / "sc-ironhail-fxout.html"),
        ("lightkeeper-fxout", REPO / "02-chain" / "sc-lightkeeper-fxout.html"),
        ("lodestone-b205-fx", REPO / "02-chain" / "sc-lodestone-b205-fx.html"),
        ("widowmaker-fxout", REPO / "02-chain" / "sc-widowmaker-fxout.html"),
        ("oracle-fx", REPO / "02-chain" / "sc-oracle-fx.html"),
        ("bindweed", B / "bindweed" / "stage6-picture" / "bw-final.html"),
        ("censer", B / "censer" / "stage6-picture" / "ce-final-fx.html"),
        ("spellbreaker", B / "spellbreaker" / "stage6-picture" / "sb-final-fx.html"),
        ("aureole", B / "aureole" / "stage6-picture" / "au-final-fx.html"),
        ("coldiron", B / "coldiron" / "stage6-picture" / "ci-final.html"),
        ("ironhail", B / "ironhail" / "stage6-picture" / "ih-final-fx.html"),
        ("lightkeeper", B / "lightkeeper" / "stage6-picture" / "lk-final-fx.html"),
        ("widowmaker", B / "widowmaker" / "stage6-picture" / "wm-final-fx.html"),
        ("heartwood", B / "heartwood" / "stage6-picture" / "hw-final-fx.html")]
nok = 0; nbad = 0
for name, tip in tips:
    if not tip.exists():
        print("[4] (missing)", tip); continue
    d = CAR / name
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src, err = build_stages(tip, d, "thornwake_build.py", "sc-thornwake-carry")
    if err:
        print(f"[4] {name} ({tip.name}): {err}"); nbad += 1; continue
    s = src.read_bytes().decode("utf-8")
    same_as_base = s == base
    try:
        a = apply(s, R2); b = apply(s, R2[::-1]); P.syntax_check(a)
        nok += 1
        print(f"[4] on {tip.name} ({sha(tip.read_bytes())}) + thornwake stages 1-5 ({sha(s)}{', = the base' if same_as_base else ''}): "
              f"every anchor once, forward == reverse {a == b}, parses (+{len(a) - len(s)} chars, the same as on the base: "
              f"{len(a) - len(s) == len(fwd) - len(base)}); SPECS.thornwake block {a.count(P.FX_BLOCK)}x; "
              f"Tendril's guard {'present' if 'f.twineHeld > 0' in a else 'absent'}")
        if V is not None:
            x = apply(apply(s, V), R2); y = apply(apply(s, R2), V); P.syntax_check(x)
            print(f"    with Thornwake's {len(V)} voice rows: voice-then-picture == picture-then-voice {x == y}, parses")
        for f in d.glob("*.html"): f.unlink()
    except (AssertionError, SystemExit) as e:
        print(f"[4] on {tip.name}: FAILS -- {e}"); nbad += 1
print(f"[4] {nok} carries clean, {nbad} failed")

# [4b] with Heartwood's picture rows (both freeze redesigns carried)
if HW is not None:
    for name, tip in (("t3", REPO / "02-chain" / "sc-tendril-t3.html"), ("spellbreaker-fxout", REPO / "02-chain" / "sc-spellbreaker-fxout.html")):
        d = CAR / ("hw+tw-" + name)
        if d.exists(): shutil.rmtree(d)
        d.mkdir()
        s1, err = build_stages(tip, d, "heartwood_build.py", "sc-heartwood-carry")
        if err:
            print(f"[4b] {name}: {err}"); continue
        s2, err = build_stages(s1, d, "thornwake_build.py", "sc-thornwake-carry")
        if err:
            print(f"[4b] {name}: {err}"); continue
        s = s2.read_bytes().decode("utf-8")
        try:
            x = apply(apply(s, HW), R2); y = apply(apply(s, R2), HW); P.syntax_check(x); P.syntax_check(y)
            import collections
            same_lines = collections.Counter(x.split(chr(10))) == collections.Counter(y.split(chr(10)))
            print(f"[4b] {tip.name} + heartwood 1-5 + thornwake 1-5 ({sha(s)}), Heartwood's {len(HW)} picture rows ({sha(HWP.read_bytes())}) "
                  f"and these, both orders: every anchor once, both parse; byte-identical {x == y}; the same lines (a multiset: "
                  f"the rows sharing an anchor land in the other order) {same_lines}; {len(x) - len(s)} chars added both ways {len(x) == len(y)}")
        except (AssertionError, SystemExit) as e:
            print(f"[4b] {name}: FAILS -- {e}")
        for f in d.glob("*.html"): f.unlink()

# [5]
try:
    apply(base, [dict(R2[0], anchor="c.fill();")]); print("[5] CONTROL DID NOT BITE")
except AssertionError as e:
    print(f"[5] CONTROL (an anchor that occurs many times) refused: {e}")
