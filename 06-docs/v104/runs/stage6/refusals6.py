#!/usr/bin/env python
"""STAGE 6's REFUSALS (v104 §5e). The real builder refuses to go on twice and
on the wrong stage; scratch copies of the builder, each with ONE S6 row
mutated, must each be refused by the rule that names it; the unmutated copy,
given the same call, must write the link byte for byte (the control).
Usage: refusals6.py  (paths fixed below; writes only under s6/refuse6/)"""
import hashlib, pathlib, subprocess, sys
PY = sys.executable
S = pathlib.Path(__file__).resolve().parent
B = pathlib.Path("C:/dev/sundered-crown/tools/angelus_build.py")
L = S.parent / "links"
OUT = S / "refuse6"
src = B.read_text(encoding="utf-8")
b9, heal, fx = L / "sc-angelus-b9.html", L / "sc-angelus-heal.html", L / "sc-angelus-b9-fx.html"
WANT = "6356f75eb0b328e1"

def run(builder, stage, s, o):
    p = subprocess.run([PY, str(builder), "--stage", stage, "--src", str(s), "--out", str(o)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = p.stderr.strip().splitlines() or ["(no stderr)"]
    ref = [ln for ln in lines if "REFUSING" in ln or "refusing" in ln]
    msg = ref[0] if ref else lines[-1]      # a refusal may carry the insert after its first line
    return p.returncode, msg

def mut(old, new):
    assert src.count(old) == 1, (src.count(old), old[:80])
    return src.replace(old, new, 1)

HEAL_LINE = "        f.ascendHeal = 0;                                       // the halo flares\n"
MOTES = '    c.fillStyle = "#FFF1CC";\n    for (let j = 0; j < 8; j++){\n'
CLOSE = ('        if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){\n'
         '          SFX.play("ult", { w: "angelus-close" });')
FALLBACK = "        } else {                                        // rune-crack'''),"
TICK = "  tickAscend(dt){\n    for (const f of [this.a, this.b]){\n"
M = {
  "picwrite  (the picture's heal flare writes foe.vx)":
      (mut(HEAL_LINE, HEAL_LINE + "        (f === this.a ? this.b : this.a).vx += 1e-9;\n"), "writes"),
  "rng       (the motes draw the RNG)":
      (mut(MOTES, MOTES.replace("{\n", "{\n      const jit = m.rng();\n")), "draws the RNG"),
  "ultfx     (tickAscend reads the one ultFx slot)":
      (mut(TICK, TICK + "      if (this.ultFx) {}\n"), "ultFx"),
  "voice     (the motes play the tap)":
      (mut(MOTES, MOTES.replace("{\n", '{\n      SFX.play("ult", { w: "angelus-shaft", n: 1 });\n')), "plays a voice outside"),
  "chord     (the close chord on every close, a death's included)":
      (mut(CLOSE, CLOSE.replace("Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive", "Z.t >= Z.dur || !f.alive")),
       "is not its voice call alone"),
  "fallback  (the shared rune-crack fallback not re-emitted)":
      (mut(FALLBACK, "        } else {                                        // (the fallback, dropped)'''),"), "rune-crack fallback"),
}
OUT.mkdir(parents=True, exist_ok=True)
rows, ok = [], True
# the real builder
rc, msg = run(B, "6", fx, OUT / "sc-angelus-twice.html")
good = rc != 0 and "already in this source" in msg and not (OUT / "sc-angelus-twice.html").exists()
rows.append(("REAL   stage 6 on the stage-6 link (twice)", rc, msg, good)); ok &= good
rc, msg = run(B, "6", heal, OUT / "sc-angelus-onheal.html")
good = rc != 0 and "stage 6 goes on stage 5" in msg and not (OUT / "sc-angelus-onheal.html").exists()
rows.append(("REAL   stage 6 on stage 3's link (the blade not 9)", rc, msg, good)); ok &= good
rc, msg = run(B, "6", b9, fx)
good = rc != 0 and "refusing to overwrite" in msg
rows.append(("REAL   stage 6 onto the existing link (overwrite)", rc, msg, good)); ok &= good
# the mutated copies
for i, (k, (txt, need)) in enumerate(M.items()):
    bp = OUT / f"angelus_build_mut{i}.py"
    bp.write_text(txt, encoding="utf-8", newline="\n")
    o = OUT / f"sc-angelus-mut{i}.html"
    rc, msg = run(bp, "6", b9, o)
    good = rc != 0 and need in msg and not o.exists()
    rows.append((f"MUTANT {k}", rc, msg, good)); ok &= good
# the control: the unmutated builder, copied, the same call
bp = OUT / "angelus_build_copy.py"
bp.write_text(src, encoding="utf-8", newline="\n")
o = OUT / "sc-angelus-control.html"
if o.exists(): o.unlink()
rc, msg = run(bp, "6", b9, o)
h = hashlib.sha256(o.read_bytes()).hexdigest()[:16] if o.exists() else "-"
good = rc == 0 and h == WANT
rows.append((f"CONTROL the unmutated copy writes the link ({h}, want {WANT})", rc, "written" if rc == 0 else msg, good)); ok &= good
print(f"STAGE 6 REFUSALS  builder {hashlib.sha256(src.encode()).hexdigest()[:16]}\n")
for k, rc, msg, good in rows:
    print(f"  {'ok  ' if good else 'FAIL'}  {k}\n        exit {rc}: {msg[:220]}")
n = sum(1 for r in rows if r[3])
print(f"\n  {n}/{len(rows)}")
if o.exists(): o.unlink()
sys.exit(0 if ok else 1)
