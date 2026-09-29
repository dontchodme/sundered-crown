"""THIRD REVIEW ROUND: negative test of lightkeeper_build.py's shared-table refusal. Scratch copies of the builder
with one write put into the tickLightwall insert (after `T.blocks++;`); each must REFUSE, and the clean copy must
write the stage-2 link byte-identical to the real one (a22bc1f8cb4b2dfe)."""
import pathlib, subprocess, hashlib, shutil, sys
G = pathlib.Path(__file__).parent
SRC = pathlib.Path("C:/dev/sundered-crown/tools/lightkeeper_build.py")
STUB = sys.argv[1]
PY = "C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
ANCH = "      T.blocks++;\n"
CASES = {
    "g_ok": None,
    "g_status": "      STATUS.ward.cap = 120;\n",          # the reviewer's v4-global, character for character
    "g_alias": "      W.cap = 120;\n",                     # through the insert's own alias, const W = STATUS.ward
    "g_config": "      CONFIG.physics.ballR += 1;\n",
    "g_aff": "      AFFINITIES[f.w.id] = null;\n",
    "g_weapons": "      WEAPONS[0].dmg = 1;\n",
    "g_shapes": "      delete SHAPES._fxc;\n",
    "g_incr": "      STATUS.ward.cap++;\n",
    "g_assign": "      Object.assign(STATUS.ward, { cap: 120 });\n",
    "g_wincr": "      f.w.dmg++;\n",
    "g_stunincr": "      foe.stun++;\n",
}
(G / "tools").mkdir(exist_ok=True); (G / "02-chain").mkdir(exist_ok=True)
s0 = SRC.read_text(encoding="utf-8")
assert s0.count(ANCH) == 1
for name, add in CASES.items():
    s = s0 if add is None else s0.replace(ANCH, ANCH + add, 1)
    p = G / "tools" / f"{name}.py"
    p.write_text(s, encoding="utf-8", newline="\n")
    out = G / f"sc-lightkeeper-{name}.html"
    if out.exists(): out.unlink()
    r = subprocess.run([PY, str(p), "--stage", "2", "--src", STUB, "--out", str(out)], capture_output=True, text=True)
    last = (r.stdout + r.stderr).strip().splitlines()[-1]
    wrote = out.exists()
    h = hashlib.sha256(out.read_bytes()).hexdigest()[:16] if wrote else "-"
    verdict = ("WRITES " + h) if wrote else "REFUSES"
    ok = (add is None and h == "a22bc1f8cb4b2dfe") or (add is not None and not wrote)
    print(f"{name:<11} {('+ ' + add.strip()) if add else '(clean copy)':<48} {verdict:<24} {'ok' if ok else 'WRONG'}   {last[:110]}")
