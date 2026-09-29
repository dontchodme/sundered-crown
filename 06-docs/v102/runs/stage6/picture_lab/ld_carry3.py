"""R3 CARRY RE-CHECK on the batch line's tip AS IT IS NOW (Coldiron carried, Ironhail being carried): Lodestone's
stages 1,2,3,5 rebuilt by tools/lodestone_build.py --src <tip> (read-only use, output in scratch carry3/), then the
picture rows (rows_final.json, re-read from disk) forward and reverse, and with Lodestone's voice rows
(stage6-voice/rows_final.json) in both orders: every anchor once, byte-identical both ways, node --check, the same
chars added as on the base. No browser. usage: ld_carry3.py"""
import hashlib, json, pathlib, subprocess, sys, shutil
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import ld_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
REPO = pathlib.Path(r"C:\dev\sundered-crown")
B = HERE.parent.parent
R = json.loads((HERE / "rows_final.json").read_bytes().decode("utf-8"))
VP = B / "lodestone" / "stage6-voice" / "rows_final.json"
V = json.loads(VP.read_bytes().decode("utf-8")) if VP.exists() else None
base = P.src_text()
dbase = len(P.apply_all(base, R)) - len(base)


def apply(src, rows):
    for r in rows:
        n = src.count(r["anchor"])
        if n != 1:
            raise AssertionError(f"{r['label']}: anchor found {n}x")
        src = P.one(src, r["anchor"], r["code"], r["mode"], r["label"])
    return src


tips = [REPO / "02-chain" / "sc-coldiron-temper-fx.html", REPO / "02-chain" / "sc-ironhail-sunder-fx.html",
        REPO / "02-chain" / "sc-ironhail-fxout.html"]
CAR = HERE / "carry3"; CAR.mkdir(exist_ok=True)
allok = True
for tip in tips:
    d = CAR / tip.stem
    if d.exists(): shutil.rmtree(d)
    d.mkdir()
    src = tip; ok = True
    for st in "1235":
        o = d / f"sc-lodestone-carry-s{st}.html"
        p = subprocess.run([PY, str(REPO / "tools" / "lodestone_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(REPO / "tools"))
        if p.returncode != 0 or not o.exists():
            print(f"{tip.name}: lodestone_build stage {st} REFUSED/FAILED: {(p.stdout + p.stderr).strip()[-400:]}"); ok = False; break
        src = o
    if not ok:
        allok = False; continue
    s = src.read_bytes().decode("utf-8")
    try:
        a = apply(s, R); b = apply(s, R[::-1]); P.syntax_check(a)
        line = (f"{tip.name} ({hashlib.sha256(tip.read_bytes()).hexdigest()[:16]}) + lodestone 1,2,3,5 "
                f"({hashlib.sha256(s.encode()).hexdigest()[:16]}): every anchor once, forward == reverse {a == b}, parses, "
                f"+{len(a) - len(s)} chars (base +{dbase}: {len(a) - len(s) == dbase})")
        good = a == b and len(a) - len(s) == dbase
        if V is not None:
            x = apply(apply(s, V), R); y = apply(apply(s, R), V); P.syntax_check(x)
            line += f"; with the {len(V)} voice rows both orders equal {x == y}, parses"
            good = good and x == y
        print(line); allok = allok and good
    except (AssertionError, SystemExit) as e:
        print(f"{tip.name}: FAILS -- {e}"); allok = False
print("CARRY3", "PASS" if allok else "FAIL")
