"""Scratch: do rows_final.json apply, unchanged, to Heartwood carried onto a later tip that carries
other relics' new voices (Tendril's among them), and do they behave there as on b11?

    python carry_check.py <tip.html>

1. heartwood_build.py --stage 5 --src <tip> --out carry/sc-heartwood-b11-<tip>.html (scratch, written once)
2. rows_final.json applied AS TEXT (each anchor exactly once before and after)
3. browser 1 (the carried link, unpatched): every other voice, the tip's own ult/bindweed-root vs
   Tendril's arm body from sc-tendril-fx, the fights; closed
4. browser 2 (the carried link + rows): every other voice unchanged, the two new voices == the lab's
   candidate text, fights identical, voice counts
"""
import hashlib, json, pathlib, subprocess, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
import numpy as np
import heartwood_voice_lab as H
from zenith_voice_lab import NOISE_SEEDS, T0, pcm
from ironwood_voice_lab import RENDER_JS
from scpage import game

PY = "C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
S = pathlib.Path(__file__).parent
tip = pathlib.Path(sys.argv[1]).resolve()
rows = json.loads((S / "rows_final.json").read_text(encoding="utf-8"))
run = json.loads((S / "run_final.json").read_text(encoding="utf-8"))
cd = S / "carry"; cd.mkdir(exist_ok=True)
link = cd / f"sc-heartwood-b11-on-{tip.stem}.html"
if not link.exists():
    src = tip
    for st, nm in (("1", "stub"), ("2", "root"), ("3", "rootfast"), ("5", "b11")):
        o = link if st == "5" else cd / f"sc-heartwood-{nm}-on-{tip.stem}.html"
        if not o.exists():
            r = subprocess.run([PY, "heartwood_build.py", "--stage", st, "--src", str(src), "--out", str(o)],
                               cwd="C:/dev/sundered-crown/tools", capture_output=True, text=True)
            print(r.stdout[-600:], r.stderr[-600:])
            if r.returncode:
                raise SystemExit("the builder refused")
        src = o
html = link.read_text(encoding="utf-8")
print(f"tip {tip.name} {hashlib.sha256(tip.read_bytes()).hexdigest()[:16]} -> carried {link.name} "
      f"{hashlib.sha256(html.encode()).hexdigest()[:16]}")
patched = html
for r_ in rows:
    c = patched.count(r_["anchor"])
    print(f"  anchor of '{r_['label'][:60]}': {c} time(s) in the carried link")
    if c != 1:
        raise SystemExit("an anchor is not there exactly once")
    patched = patched.replace(r_["anchor"], r_["code"], 1)
for r_ in rows:
    if patched.count(r_["anchor"]) != 1:
        raise SystemExit("an anchor is not re-emitted exactly once")
pp = cd / f"sc-heartwood-voices-on-{tip.stem}.html"
pp.write_text(patched, encoding="utf-8", newline="")
print(f"  patched {pp.name} {hashlib.sha256(patched.encode()).hexdigest()[:16]}")

TH = pathlib.Path("C:/dev/sundered-crown/02-chain/sc-tendril-fx.html").read_text(encoding="utf-8")
troot = H.tendril_arm(TH, "bindweed-root")[1]
csp = dict(H.CAST_CANDIDATES)[run["pick"]["cast"]] if False else [c[1] for c in H.CAST_CANDIDATES if c[0] == run["pick"]["cast"]][0]
cast_text = H.cast_body(csp, run["pick"]["cast_g"])
root_text = H.root_from_tendril(troot, run["pick"]["root_g"])
for r_ in rows:
    pass
assert cast_text in rows[0]["code"] and root_text in rows[0]["code"], "the rows are not the picks"
seeds = [112651]


def voices(page):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 11, 18, 50) for c_ in (False, True)]
    others += [("wall", {}), ("death", {}), ("ult", {"w": "bindweed-root"}), ("ult", {"w": "bindweed"}),
               ("ult", {"w": "ironwood-wither"}), ("ult", {"w": "paradox-pin"})]
    others += [("ult", {"w": w_}) for w_ in ids if w_ != "heartwood"]
    return others


def R(page, evs, seed=None):
    return pcm(page.evaluate(RENDER_JS, [evs, 3.0, seed, None]))


with game(game_path=link) as (page, errors):
    others = voices(page)
    ref = [R(page, [["play", T0, k, p]]) for k, p in others]
    tr_here = float(np.abs(R(page, [["play", T0, "ult", {"w": "bindweed-root"}]]) -
                           R(page, [["body", T0, troot, {}]])).max())
    F0 = page.evaluate(H.FIGHTS_JS, [seeds])
    assert not errors, errors[:3]
print(f"  on the carried tip, ult/bindweed-root vs Tendril's arm body read from sc-tendril-fx: max |diff| {tr_here:.1e}"
      f" -- {'the same voice: heartwood-root is it, g scaled' if tr_here < 1e-6 else 'NOT the same'}")
with game(game_path=pp) as (page, errors):
    worst = max(float(np.abs(R(page, [["play", T0, k, p]]) - x0).max()) for (k, p), x0 in zip(others, ref))
    nd = []
    for lab, w, text in (("cast", "heartwood", cast_text), ("root", "heartwood-root", root_text)):
        for sd in (NOISE_SEEDS[0], NOISE_SEEDS[7]):
            nd.append((lab, float(np.abs(R(page, [["play", T0, "ult", {"w": w}]], sd) -
                                         R(page, [["body", T0, text, {}]], sd)).max())))
    F1 = page.evaluate(H.FIGHTS_JS, [seeds])
    perr = len(errors)
A = {f["key"]: f for f in F0}
same = sum(A[f["key"]]["sum"] == f["sum"] for f in F1)
osame = sum(A[f["key"]]["other"] == f["other"] for f in F1)
tot = {k: sum(f[k] for f in F1) for k in ("casts", "rooted", "castV", "rootV", "closeV")}
print(f"  every other voice ({len(others)}), patched vs unpatched carried page: worst {worst:.1e}")
print(f"  the new voices vs the lab's candidate text: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
print(f"  {len(F1)} fights: {same}/{len(F1)} identical, other SFX identical {osame}/{len(F1)}; totals {tot}; "
      f"root voices = rooted in {sum(f['rootV'] == f['rooted'] for f in F1)}/{len(F1)}, cast voices = casts in "
      f"{sum(f['castV'] == f['casts'] for f in F1)}/{len(F1)}; page errors {perr}")
ok = (worst <= 1e-6 and max(v for _, v in nd) <= 1e-6 and same == len(F1) and osame == len(F1) and perr == 0
      and tot["rootV"] == tot["rooted"] and tot["castV"] == tot["casts"] and tot["closeV"] == 0 and tr_here < 1e-6)
print("CARRY CHECK " + ("PASS" if ok else "FAIL"))
